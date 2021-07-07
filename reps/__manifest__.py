# -*- coding: utf-8 -*-
# Part of Aselcis Consulting SL. See LICENSE file for full copyright and licensing details.

{
    "name": "REPS",
    "depends": ['cgcof_contact_fields','data_file_generator'],
    "author": "Aselcis consulting",
    "category": "",
    "website": "https://www.aselcis.com",
    "description": """
    Reps data system
""",
    "data": [
        "data/reps_cron.xml",
        "views/reps_menu.xml",
        "views/reps_history_view.xml",
        "views/data_file_generator_menu.xml",
        "views/file_data_template_view.xml",
        "views/reps_azure_file_view.xml",
        "views/azure_blobs.xml",
        "security/ir.model.access.csv"
    ],
    'qweb': [
    ],
    "installable": True,
    'application': True
}
