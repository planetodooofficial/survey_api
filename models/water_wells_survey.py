# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class water_well_survey(models.Model):
    _name = 'water.well.survey'
    _rec_name = 'water_well_survey_id'

    water_well_survey_id = fields.Integer('Survey ID')
    district = fields.Char('District')
    TA = fields.Char('TA')
    village_name = fields.Char('Village Name')
    first_last_name_chief = fields.Char('First & Last name of Chief')
    date = fields.Date('Date')
    well_gps_longitude = fields.Char('Well Location Longitude')
    well_gps_latitude = fields.Char('Well Location Latitude')
    id_number_well = fields.Char('180 ID Number of well')
    well_image_1 = fields.Binary('Photo of Well')
    well_image_2 = fields.Binary('Photo of well with 180 sticker + pump id number clearly visible')
    well_image_3 = fields.Binary('Photo of well with people using it')
    comments_1 = fields.Text("Comments")
    comments_2 = fields.Text("Comments")

