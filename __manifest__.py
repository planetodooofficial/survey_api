# -*- coding: utf-8 -*-
{
    'name': 'Survey Details',
    'Version': '13.0.1',
    'category': 'Survey',
    'Author': 'Planet Odoo',
    'Company': 'Planet Odoo',
    'Website': 'http://www.planet-odoo.com/',
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/farmer_survey_view.xml',
        'views/tree_survey_view.xml',
        'views/cook_stove_survey.xml',
        'views/water_well_survey.xml',
    ],
    'installable': True,
    'auto_install': False,

}
