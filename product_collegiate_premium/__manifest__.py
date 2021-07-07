# -*- coding: utf-8 -*-
# Part of Aselcis Consulting SL. See LICENSE file for full copyright and licensing details.

{
    "name": "Product collegiate premium",
    "depends": ['product', 'website_sale', 'cgcof_contact_fields'],
    "author": "Aselcis consulting",
    "category": "Product",
    "website": "https://www.aselcis.com",
    "description": """
    Product collegiate premium
""",
    "data": [
        "views/product_template_view.xml",
        "views/res_config_settings_views.xml",
        "security/ir.model.access.csv"
        # "views/templates.xml",
        # "views/website_sale_templates.xml"
    ],
    'qweb': [
    ],
    "installable": True,
}
