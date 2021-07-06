# -*- coding: utf-8 -*-

{
    'name': 'acceso',
    
    'sumary': """ Recuperar Cuenta desde Portalfarma""",
    
    'description': """ Si usuario existe en Portalfarma y contraseña coincide, asignamos dicha contraseña al usuario en Odoo para que tenga acceso. """,
    
    'author': 'AMP Software - Dani G.',
    
    'Website': 'https://www.ampsoftware.com',
    
    'category': 'Website',
    
    'version': '1.0',
    
    'depends': [
        'website',
        'web',
    ],
    
    'data': [
        'views/acceso_templates.xml'
    ],
    
    'demo': [
    ],
}