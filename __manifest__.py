# -*- coding: utf-8 -*-
{
    'name': 'Survey Details',
    'Version': '13.0.1',
    'category': 'Survey',
    'Author': 'Planet Odoo',
    'Company': 'Planet Odoo',
    'Website': 'http://www.planet-odoo.com/',
    'depends': ['base', 'product', 'contacts', 'stock', 'website','sale'],

    'data': [
        'data/stock_quant_view.xml',
        'data/stock_picking_type_dropship_view.xml',
        'security/ir.model.access.csv',
        'views/farmer_survey_view.xml',
        'wizard/product_batch_split_wizard.xml',
        'wizard/api_wizard_view.xml',
        'wizard/stock_move_location.xml',
        'wizard/stock_scrap_inherit_for_wizard_view.xml',
        'views/res_partner_view_inherit.xml',
        'views/tree_survey_view.xml',
        'views/cook_stove_survey.xml',
        'views/water_well_survey.xml',
        'views/district_village_view.xml',
        # 'views/custom_css.xml',
        'views/stock_picking_type_views.xml',
        'views/product_batch_split.xml',
        'views/configuration_view.xml',
    ],
    'installable': True,
    'auto_install': False,

}
