# -*- coding: utf-8 -*-

{
    "name": "Juntas Gobierno",

    "summary": "Gestion de la Junta de Gobierno, Colegio Oficial de Farmacéuticos",

    "description": """Modulo CGF Juntas de Gobierno""",

    "author": "vfperez",

    "website": "https://ampsoftware.com",

    "category": "Administration",
    "version": "0.1",

    "depends": [
        "base",
        "sale",
        "mail",
        
    ],

    "data": [
        "security/ir.model.access.csv",
        "views/vista_cambiar.xml",
        "views/sale.xml",
        "data/sequence.xml",
    ],
}