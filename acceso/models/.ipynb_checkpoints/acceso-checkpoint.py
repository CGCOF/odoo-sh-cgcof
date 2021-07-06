# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class Acceso(models.Model):

    _inherit = 'website'
    