# -*- coding: utf-8 -*-

from odoo import models, api, fields

class Cargos_Jg(models.Model):
    _name = "cargos.jg"
    _description = "Cargos Junta Gobierno"

    x_identificador = fields.Integer(string="Identificador")
    x_descripcion = fields.Char(string="Descripción")