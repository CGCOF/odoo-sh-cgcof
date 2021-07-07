# -*- coding: utf-8 -*-
# Part of Aselcis Consulting SL. See LICENSE file for full copyright and licensing details.

from odoo import models, api
from odoo.osv import expression


class Website(models.Model):
    _inherit = 'website'

    @api.multi
    def sale_product_domain(self):
        res = super(Website, self).sale_product_domain()
        user_id = self.env['res.users'].browse([self._uid])
        partner_id = user_id['partner_id'] or False
        if partner_id and partner_id._type == 'collegiate' and partner_id.collegiate_id.is_active() and partner_id.collegiate_id.enabled or partner_id._type == 'college':
            res = expression.AND([res, [('premium', '=', True)]])
        return res
