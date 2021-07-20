# -*- coding: utf-8 -*-

from odoo import models, api, fields, _

class CargosColegio(models.Model):
    _name = "cargos.colegio"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Cargos Junta Gobierno Colegios"
    _rec_name = 'x_nombre'

    x_id_cargos = fields.Integer(string="ID del Cargo")
    x_id_colegios = fields.Integer(string="ID del Colegio")
    x_id_puestos = fields.Integer(string="ID del Partner")
    x_cargos_jg = fields.Char(string="Cargo JG", required=True)#esto cambiarlo por un many2one o el que sea.
    x_dni = fields.Char(string="DNI", required=True)
    x_nombre = fields.Char(string="Nombre", required=True)
    x_apellidos = fields.Char(string="Apellidos")
    x_indicadorERP = fields.Boolean(string="Indicador ERP")
    x_fechaI = fields.Date(string="Fecha Inicio")
    x_fechaF = fields.Date(string="Fecha Fin")
    x_seq = fields.Char(string="Orden", required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    
    @api.model
    def create(self, vals):
        if vals.get('x_seq', _('New')) == ('New'):
            vals['x_seq'] = self.env['ir.sequence'].next_by_code('cargos.colegio.sequence') or _('New')
            result = super(CargosColegio, self).create(vals)
            return result