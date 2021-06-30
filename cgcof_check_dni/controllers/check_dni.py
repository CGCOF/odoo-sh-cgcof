# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class CheckDni(http.Controller):
    _inerit = 'res.users'
    @http.route('/check', auth='none', website=True)
    def check_dni(self, **kw):
        db = 'cgcof-odoo-sh-cgcof-staging-817321'
        login = '00000000V'
        password = 'toor'
        request.session.authenticate(db, login, password)
        dni = request.params['dni']
        user = http.request.env['res.users'].search([('dni', '=', dni)])
        print("hola estoy en la funcion reset_password por i1nherit")
        print(user)
        print(type(user))
        if len(user) != 1:
            return "no existe el correo introducido"
        else:
            print("usuario existente en BDD")