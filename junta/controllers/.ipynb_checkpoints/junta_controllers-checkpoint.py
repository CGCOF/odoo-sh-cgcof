# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class Junta(http.Controller):
    @http.route('/junta_gobierno', auth='public', website=True)
    def carga_datos(self, **kw):
        
        user_id = request.params['user']
        """
        db = 'cgcof-odoo-sh-cgcof-dani-2906786'
        login = 'admin'
        password = 'admin'
        request.session.authenticate(db, login, password)
        
        colegio = http.request.env['res.college'].search([('collegiate', '=', user_id)])
        
        nombre_colegio = colegio.id
        
        return nombre_colegio
        """
        return http.request.render('junta.home_junta_gobierno',{})
    
    """
    @http.route('/acceso_desde_portalfarma_ko', auth='public', website=True)
    def acceso_ko(self, **kw):
        
        return http.request.render('acceso.acceso_desde_portalfarma_ko',{})
    
    @http.route('/acceso_desde_portalfarma_ok', auth='public', website=True)
    def acceso_ok(self, **kw):
        
        userDNI = request.params['usd']
        userPass = request.params['userPass']
        
        db = '(danielguerracarrascosa-doce-main-2743393'
        login = 'admin'
        password = 'admin'
        request.session.authenticate(db, login, password)
        
        user = http.request.env['res.users'].search([('login', '=', userDNI)])
        id_user = user.id
        
        user = http.request.env['res.users'].browse(id_user)
        user.password = userPass
        http.request.env.cr.commit()
        
        return http.request.render('acceso.cuenta_recuperada_portalfarma',{'dni':userDNI})
        """