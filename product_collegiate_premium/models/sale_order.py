from odoo import models, api, fields, _


WARNIGN_MSG = _('''
A collegiate-type customer cannot purchase a non-premium product, 
so such products will be removed from the budget
''')

class SaleOrderProductRemove(models.Model):

    _name = 'sale.order.product.remove'

    product_id = fields.Many2one('product.product')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    remove_product_ids = fields.Many2many('sale.order.product.remove')

    @api.onchange('partner_id', 'order_line')
    def _onchange_partner_order_line(self):
            if self.partner_id._type == 'collegiate' and \
                    self.partner_id.collegiate_id and \
                    self.partner_id.collegiate_id.is_active() and \
                    self.partner_id.collegiate_id.enabled or \
                    self.partner_id._type == 'college':
                not_premium_lines = self.order_line.filtered(
                    lambda ol: not ol.product_id.premium)
                if not_premium_lines:
                    self.order_line = self.order_line.filtered(
                        lambda ol: ol not in not_premium_lines)
                    warning_mess = {
                        'title': _('Restriction!'), 
                        'message': WARNIGN_MSG}
                    return {'warning': warning_mess}

    @api.constrains('partner_id', 'order_line', 'partner_invoice_id')
    def check_partner_id_product_premium(self):
        if self.partner_id._type == 'collegiate' and \
                self.partner_id.collegiate_id and \
                self.partner_id.collegiate_id.is_active() and \
                self.partner_id.collegiate_id.enabled or \
                self.partner_id._type == 'college':
            not_premium_lines = self.order_line.filtered(
                lambda ol: not ol.product_id.premium)
            if not_premium_lines:
                self.write({'remove_product_ids':
                            [(0, 0, {'product_id': line.product_id.id})
                             for line in not_premium_lines]
                            })
                not_premium_lines.unlink()
                raise Warning(WARNIGN_MSG)
