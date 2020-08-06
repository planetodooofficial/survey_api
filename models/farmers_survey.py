# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class farmer_survey(models.Model):
    _name = 'farmer.survey'
    _rec_name = 'farmer_survey_id'

    farmer_survey_id = fields.Integer('Survey ID')
    district = fields.Char('District')
    epa = fields.Char('EPA')
    village = fields.Char('Village', required=True)
    farmer_name = fields.Char("Farmer's Name", required=True)
    farmer_id = fields.Char("Farmer's 180 ID")
    farmer_photo_1 = fields.Binary("Farmer's Photo 1 (Whole body in front of hut)", required=True)
    farmer_photo_2 = fields.Binary("Farmer's Photo 2 (Whole body in front of hut)", required=True)
    farmer_photo_3 = fields.Binary("Farmer's Photo 3 (Whole body ideally next to trees)")
    farmer_photo_4 = fields.Binary("Farmer's Photo 4 (With whole family)")
    farmer_photo_5 = fields.Binary("Farmer's Photo 5 (Clear image of multiple trees of the farmer with whole family)")
    farmer_national_id = fields.Char("Farmer's National ID")
    farmer_age = fields.Integer("Farmer's Age")
    is_married = fields.Selection([('Yes', 'yes'), ('No', 'no')], string='Married')
    farmer_wife_name = fields.Char("Wife's Name")
    farmer_wife_age = fields.Integer("Wife's Age")
    farmer_children = fields.Integer("No. Of Children")
    no_of_kids_ids = fields.One2many('farmer.kids.details', 'farmer_kids_details_id', string="No. Of Kids")
    farmer_farming_list = fields.Char('List of Products Farmer Farming on his fields')
    farmer_fruit_trees = fields.Selection([('Yes', 'yes'), ('No', 'no')], string='Does the farmer grow fruit trees?')
    no_of_tres_for_planting = fields.Integer('How many trees would the farmer like to plant?')
    efficient_cook_stove = fields.Selection([('Yes', 'yes'), ('No', 'no')],
                                            string='Does he have an energy efficient cook-stove??')
    get_firewood_from = fields.Char("Where does the farmer get firewood now? ")
    hours_taken_per_week = fields.Float('How many hours does this take per week?')
    comments = fields.Text('Comments')
    special_info_farmer = fields.Text('Special information about farmer')


class farmer_kids_details(models.Model):
    _name = 'farmer.kids.details'

    farmer_kids_details_id = fields.Many2one('farmer.survey', "Farmer's Kids ID")
    farmer_kid_name = fields.Char('Name')
    farmer_kid_age = fields.Char('Age')
    farmer_kid_gender = fields.Char('Gender')
