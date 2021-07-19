# -*- coding: utf-8 -*-

from odoo import models, api, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    sale_description = fields.Char(string="Sale Description1")