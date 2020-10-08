# -*- coding: utf-8 -*-
{
    'name': 'Survey Details',
    'Version': '13.0.1',
    'category': 'Survey',
    'Author': 'Planet Odoo',
    'Company': 'Planet Odoo',
    'Website': 'http://www.planet-odoo.com/',
    'depends': ['base', 'product', 'contacts', 'stock', 'website'],

    'data': [
        'data/stock_quant_view.xml',
        'security/ir.model.access.csv',
        'views/farmer_survey_view.xml',
        'views/tree_survey_view.xml',
        'views/cook_stove_survey.xml',
        'views/water_well_survey.xml',
        'views/district_village_view.xml',
        'views/custom_css.xml',
        'views/stock_picking_type_views.xml',
        'views/product_batch_split.xml',
        'wizard/product_batch_split_wizard.xml',
        'wizard/stock_move_location.xml',
    ],
    'installable': True,
    'auto_install': False,

}
