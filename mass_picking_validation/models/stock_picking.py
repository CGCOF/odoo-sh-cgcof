# -*- coding: utf-8 -*-
# Part of Aselcis. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.depends('state', 'move_lines.move_line_ids.product_uom_qty')
    def _compute_reserved_percentage(self):
        for picking in self:
            if picking.state not in ['draft', 'done', 'cancel'] and picking.move_lines:
                all_uom_qty = 0
                all_reserved_qty = 0
                for line in picking.move_lines:
                    all_uom_qty += line.product_uom_qty
                    all_reserved_qty += line.reserved_availability            # If still in draft => confirm and assign

                dividend = (
                    all_reserved_qty / all_uom_qty) if picking.move_lines and all_uom_qty > 0 else 0
                picking.reserved_percentage = dividend * 100

    reserved_percentage = fields.Float(
        string='Reserved percentage', compute='_compute_reserved_percentage', store=True)


class Picking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_assign(self):
        if self:
            super(Picking, self).action_assign()
        if not self:    
            for record in self._context['active_ids']:
                picking_id = self.env['stock.picking'].browse(record)
                moves = picking_id.mapped('move_lines').filtered(
                    lambda move: move.state not in ('draft', 'cancel', 'done'))
                if not moves:
                    raise UserError(
                        _(str(picking_id.name)+'\nNothing to check the availability for.'))
                if picking_id.state not in ['assigned', 'confirmed']:
                    raise UserError(
                        _(str(picking_id.name)+'\nPicking state invalid.'))
                super(Picking, picking_id).action_assign()

    @api.multi
    def button_validate(self):
        if self:
            return super(Picking, self).button_validate()
        if not self:    
            picking_ids = [self.env['stock.picking'].browse(record) for record in self._context['active_ids']]
            for picking_id in picking_ids:
                if picking_id.reserved_percentage != 100:
                    raise UserError(
                        _(str(picking_id.name)+'\nYou cannot validate a transfer if no quantites are reserved nor done. To force the transfer, switch in edit more and encode the done quantities.'))
                if picking_id.state not in ['assigned']:
                    raise UserError(
                        _(str(picking_id.name)+'\nPicking state invalid'))
                picking_id.ensure_one()
                if not picking_id.move_lines and not picking_id.move_line_ids:
                    raise UserError(
                        _(str(picking_id.name)+'Please add some items to move.'))

                # If no lots when needed, raise error
                picking_type = picking_id.picking_type_id
                precision_digits = picking_id.env['decimal.precision'].precision_get(
                    'Product Unit of Measure')
                no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits)
                                        for move_line in picking_id.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
                no_reserved_quantities = all(float_is_zero(
                    move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in picking_id.move_line_ids)
                if no_reserved_quantities and no_quantities_done:
                    raise UserError(
                        _('You cannot validate a transfer if no quantites are reserved nor done. To force the transfer, switch in edit more and encode the done quantities.'))

                if picking_type.use_create_lots or picking_type.use_existing_lots:
                    lines_to_check = picking_id.move_line_ids
                    if not no_quantities_done:
                        lines_to_check = lines_to_check.filtered(
                            lambda line: float_compare(line.qty_done, 0,
                                                    precision_rounding=line.product_uom_id.rounding)
                        )

                    for line in lines_to_check:
                        product = line.product_id
                        if product and product.tracking != 'none':
                            if not line.lot_name and not line.lot_id:
                                raise UserError(
                                    _('You need to supply a Lot/Serial number for product %s.') % product.display_name)

                if no_quantities_done:
                    picking_id.validate_massive_process()
                self.action_done()        
            return 

    def validate_massive_process(self):
        pick_to_backorder = self.env['stock.picking']
        pick_to_do = self.env['stock.picking']
        for picking in self:
            if picking.state == 'draft':
                picking.action_confirm()
                if picking.state != 'assigned':
                    picking.action_assign()
                    if picking.state != 'assigned':
                        raise UserError(_("Could not reserve all requested products. Please use the \'Mark as Todo\' button to handle the reservation manually."))
            for move in picking.move_lines.filtered(lambda m: m.state not in ['done', 'cancel']):
                for move_line in move.move_line_ids:
                    move_line.qty_done = move_line.product_uom_qty
            if picking._check_backorder():
                pick_to_backorder |= picking
                continue
            pick_to_do |= picking
        if pick_to_do:
            pick_to_do.action_done()
        if pick_to_backorder:
            return pick_to_backorder.action_generate_backorder_wizard()
        return False    

