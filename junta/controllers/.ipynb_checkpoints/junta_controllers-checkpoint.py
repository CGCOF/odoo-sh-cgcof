# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class Junta(http.Controller):
    
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
    @http.route('/junta_gobierno/<model("res.partner"):collegiate_id>', auth='public', website=True)
    def carga_datos(self, collegiate_id):
        return http.request.render('junta.home_junta_gobierno',{
            "collegiate": collegiate_id
        })
        """