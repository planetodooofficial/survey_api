# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class tree_survey(models.Model):
    _name = 'tree.survey'
    _rec_name = 'tree_survey_id'

    tree_survey_id = fields.Integer('Survey ID')
    scanned_farmer_id = fields.Char("Scanned Farmer's ID", required=True)
    gps_longitude = fields.Char('Longitude')
    gps_latitude = fields.Char('Latitude')
    tree_type = fields.Char('Tree Type')
    tree_image_1 = fields.Binary('Image 1', required=True)
    tree_image_2 = fields.Binary('Image 2', required=True)
    tree_image_3 = fields.Binary('Image 3')
    survey_date = fields.Date('Survey Date')

