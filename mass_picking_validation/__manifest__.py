# -*- coding: utf-8 -*-
# Part of Aselcis Consulting SL. See LICENSE file for full copyright and licensing details.

{
    "name": "Mass Picking Validation",
    "depends": ['base','stock'],
    "author": "Aselcis consulting",
    "category": "Stock",
    "website": "https://www.aselcis.com",
    "description": """
    - Mass validation of delivery pickings
    - Check pickings availability massively
    - Add filters by percentage reserve
""",
    "data": [
        "views/stock_picking_views.xml"
    ],
    'qweb': [
    ],
    "installable": True,
    'application': True
}
