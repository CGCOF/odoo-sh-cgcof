# -*- coding: utf-8 -*-
# Part of Aselcis Consulting SL. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('_type', 'college_id', 'collegiate_id')
    def onchange_type(self):
        if self._type == 'college' and self.college_id:
            config = self.env["ir.config_parameter"].sudo()
            college_pricelist, college_pricelist_id = config.get_param(
                "sale.college_pricelist"), config.get_param("sale.college_pricelist_id")
            if college_pricelist and college_pricelist_id:
                self.property_product_pricelist = int(
                    college_pricelist_id)
                self._inverse_product_pricelist()

        elif self._type == 'collegiate' and self.collegiate_id:
            config = self.env["ir.config_parameter"].sudo()
            collegiate_pricelist, dis_pricelist_id, enabled_pricelist = config.get_param(
                "sale.collegiate_pricelist"), config.get_param("sale.disabled_pricelist_id"), config.get_param("sale.enabled_pricelist_id")
            if collegiate_pricelist:
                if self.collegiate_id.enabled and self.collegiate_id.is_active() and enabled_pricelist:
                    self.property_product_pricelist = int(
                        enabled_pricelist)
                elif not self.collegiate_id.enabled or not self.collegiate_id.is_active() and dis_pricelist_id:
                    self.property_product_pricelist = int(
                        dis_pricelist_id)
                self._inverse_product_pricelist()
        