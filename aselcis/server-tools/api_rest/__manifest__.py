# -*- coding: utf-8 -*-
# Part of Aselcis. See LICENSE file for full copyright and licensing details.
{
    "name": 'API Rest',
    "summary": 'Configurable API-Rest',
    "category": 'System',
    "version": '12.0.1.0',
    "depends": ['base'],
    'external_dependencies': {
        'python': ['jwt'],
    },
    "author": "Aselcis Consulting S.L",
    "website": "https://aselcis.com",
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rules.xml",
        "data/ir_config_param.xml",
        "views/api.xml",
        "views/res_users.xml"
    ],
    "installable": True,
    "auto_install": False,
}
