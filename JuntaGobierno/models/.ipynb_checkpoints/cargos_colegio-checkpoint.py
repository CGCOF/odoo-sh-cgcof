# -*- coding: utf-8 -*-

from odoo import models, api, fields

class Cargos_Colegio(models.Model):
    _name = "cargos.colegio"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Cargos Junta Gobierno Colegios"
    _rec_name = 'x_nombre'

    x_id_cargos = fields.Integer(string="ID del Cargo")
    x_id_colegios = fields.Integer(string="ID del Colegio")
    x_id_puestos = fields.Integer(string="ID del Partner")
    x_orden = fields.Integer(string="Orden (secuencia)")
    x_cargos_jg = fields.Char(string="Cargo JG", required=True)#esto cambiarlo por un many2one o el que sea.
    x_dni = fields.Char(string="DNI", required=True)
    x_nombre = fields.Char(string="Nombre", required=True)
    x_apellidos = fields.Char(string="Apellidos")
    x_indicadorERP = fields.Boolean(string="Indicador ERP")
    x_fechaI = fields.Date(string="Fecha Inicio")
    x_fechaF = fields.Date(string="Fecha Fin")