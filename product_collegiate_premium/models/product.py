# -*- coding: utf-8 -*-
# Part of Aselcis Consulting SL. See LICENSE file for full copyright and licensing details.

from odoo import models,fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    premium = fields.Boolean()


