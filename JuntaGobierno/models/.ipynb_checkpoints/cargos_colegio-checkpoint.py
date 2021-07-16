# -*- coding: utf-8 -*-

from odoo import models, api, fields

class Cargos_Colegio(models.Model):
    _name = "cargos.colegio"
    _description = "Cargos Junta Gobierno Colegios"

    x_id_cargos = fields.Integer(string="ID del Cargo")
    x_id_colegios = fields.Integer(string="ID del Colegio")
    x_id_puestos = fields.Integer(string="ID del Partner")
    x_orden = fields.Integer(string="Orden (secuencia)")
    x_cargo_jg = fields.Integer(string="Cargo JG")#esto cambiarlo por un many2one o el que sea.
    x_dni = fields.Char(string="DNI")
    x_nombre = fields.Char(string="Nombre")
    x_apellidos = fields.Char(string="Apellidos")
    x_indicadorERP = fields.Boolean(string="Indicador ERP")
    x_fechaI = fields.Date(string="Fecha Inicio")
    x_fechaF = fields.Date(string="Fecha Fin")

