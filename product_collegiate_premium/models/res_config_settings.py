# -*- coding: utf-8 -*-
# Part of Aselcis Consulting SL. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    collegiate_pricelist = fields.Boolean(
        'Collegiate dynamic pricelist', config_parameter='sale.collegiate_pricelist')
    college_pricelist = fields.Boolean(
        'College dynamic pricelist', config_parameter='sale.college_pricelist')
    disabled_pricelist_id = fields.Many2one(
        'product.pricelist', 'Pricelist to disabled collegiates', config_parameter='sale.disabled_pricelist_id')
    enabled_pricelist_id = fields.Many2one(
        'product.pricelist', 'Pricelist to enabled collegiates', config_parameter='sale.enabled_pricelist_id')
    college_pricelist_id = fields.Many2one(
        'product.pricelist', 'Pricelist to enabled colleges', config_parameter='sale.college_pricelist_id')
