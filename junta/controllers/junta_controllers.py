# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class Junta(http.Controller):
    
    @http.route('/busca_dni', auth='public', website=True, methods=['POST', 'GET'], type='json')
    def busca_dni(self, **kw):
        dni = request.params['dni']
        
        db = 'cgcof-odoo-sh-cgcof-dani-2907548'
        login = 'pruebasD@email.com'
        password = 'admin'
        request.session.authenticate(db, login, password)
        result_dni = http.request.env['res.collegiate'].search([('vat', '=', dni)])
        
        if result_dni != "":
            return [{"nombre": result_dni.name, "apellidos": result_dni.surname, "dni": result_dni.vat}]
        else:
            array=[]
            dato = {
                "nombre": "",
                "apellidos": "",
                "dni": ""
            }
            return array
        
    @http.route('/busca_dni2', auth='public', website=True, methods=['POST', 'GET'])
    def busca_dni2(self, **kw):
        dni = request.params['dni']
        
        db = 'cgcof-odoo-sh-cgcof-dani-2907548'
        login = 'pruebasD@email.com'
        password = 'admin'
        request.session.authenticate(db, login, password)
        result_dni = http.request.env['res.collegiate'].search([('vat', '=', dni)])
        
        if result_dni != "":
            array=[]
            dato = {
                "nombre": "nombre",
                "apellidos": "apellidos",
                "dni": "dni"
            }
            array.append(dato)
            return array
        else:
            array=[]
            dato = {
                "nombre": "",
                "apellidos": "",
                "dni": ""
            }
            return array
        
    @http.route('/guarda_new', auth='public', website=True, methods=['POST'])
    def guardar_new(self, **kw):
        
        cargo = request.params['cargo']
        nombre = request.params['nombre']
        apellidos = request.params['apellidos']
        dni = request.params['dni']
        fecha_inicio = request.params['fecha_inicio']
        fecha_final = request.params['fecha_final']
        web = request.params['web']
        orden = request.params['orden']
        
        respuesta = "ok"
        
        """
        Para devolver datos con type='json'
        
        products = http.request.env['product.template'].search([('website_published', '=', True)])
        array=[]
        
        for product in  products:
            datos = {
                "name": product.name,
                "id": product.id
            }
            array.append(datos)
        
        return array
        
        """
        
        return respuesta
        
    @http.route('/pru', auth='public', website=True, methods=['GET'])
    def guardar_new(self, **kw):
        
        cargo = request.params['cargo']
        
        respuesta = "ok"
        
        return respuesta
    
    @http.route('/junta_gobierno', auth='public', website=True)
    def carga_datos(self, **kw):
        user = request.params['user']
        
        db = 'cgcof-odoo-sh-cgcof-dani-2907548'
        login = 'pruebasD@email.com'
        password = 'admin'
        request.session.authenticate(db, login, password)
        
        persona = http.request.env['res.college.collegiate'].search([('collegiate_id', '=', user)])
        
        return http.request.render('junta.home_junta_gobierno',{
            "persona": persona
        })
        
        """
        - si sirve pero no muestra nombre del colegio
        persona = http.request.env['res.college.collegiate'].search([('collegiate_id', '=', user)])
        colegio = persona.ds_soe
        numPersona = persona.collegiate_number
        
        - si sirve SIII -
        persona = http.request.env['res.collegiate'].search([('partner_id', '=', user)])
        colegio = persona.name
        
        - no accede -
        colegio = persona.college_id
        
        """
        
        return colegio
        
        """
        persona = http.request.env['res.partner'].search([('collegiate_id', '=', user)])
        
        -- no puede acceder a propiedad del objeto --
        nombre_persona = persona.collegiate_id
        
        return nombre_persona        
        """
        
        
        """
    @http.route('/junta_gobierno/<model("res.partner"):collegiate_id>', auth='public', website=True, methods=['GET', 'POST'], type='json')
    def carga_datos(self, collegiate_id):
        return http.request.render('junta.home_junta_gobierno',{
            "collegiate": collegiate_id
        })
        
        """