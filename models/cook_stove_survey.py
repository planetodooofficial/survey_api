# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class cook_stove_survey(models.Model):
    _name = 'cook.stove.survey'
    _rec_name = 'cook_stove_survey_id'

    cook_stove_survey_id = fields.Integer('Survey Id')
    farmer_id = fields.Char("Farmer's ID")
    t_a = fields.Char('T/A')
    name_of_chief = fields.Char('Name Of Chief')
    name_of_village = fields.Char('Name Of Village')
    type_of_kitchen = fields.Char('Type Of Kitchen', requried=True)
    cooking_method = fields.Char('Cooking Method', requried=True)
    have_an_axe = fields.Selection([('Yes', 'yes'), ('No', 'no')], string='Do you have an axe?', requried=True)
    per_week_walking_for_firewood = fields.Float('How many hours per week walking for firewood?', requried=True)
    stove_id = fields.Char('Stove ID')
    kitchen_gps_longitude = fields.Char('Kitchen GPS Longitude', requried=True)
    kitchen_gps_latitude = fields.Char('Kitchen GPS Latitude', requried=True)
    same_stove_used = fields.Selection([('Yes', 'yes'), ('No', 'no')], string='Is this the only stove that you use?', requried=True)
    stove_condition = fields.Selection([('Average', 'avg'), ('Yes', 'yes'), ('No', 'no')], string='Is the stove in good condition?')
    comments_1 = fields.Text('Suggestions')
    comments_2 = fields.Text('Extra Suggestions')


