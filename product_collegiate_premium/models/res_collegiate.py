# -*- coding: utf-8 -*-
# Part of Aselcis Consulting SL. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResCollegiate(models.Model):
    _inherit = 'res.collegiate'

    @api.onchange('disable_ids', 'college_ids')
    def onchange_disable_ids(self):
        config = self.env["ir.config_parameter"].sudo()
        collegiate_pricelist, dis_pricelist_id, enabled_pricelist = config.get_param(
            "sale.collegiate_pricelist"), config.get_param("sale.disabled_pricelist_id"), config.get_param("sale.enabled_pricelist_id")
        if self.partner_id and collegiate_pricelist:
            if self.enabled and self.is_active() and enabled_pricelist:
                self.partner_id.property_product_pricelist = int(
                    enabled_pricelist)
            elif not self._origin.enabled or not self._origin.is_active() and dis_pricelist_id:
                self.partner_id.property_product_pricelist = int(
                    dis_pricelist_id)
            self.partner_id._inverse_product_pricelist()
