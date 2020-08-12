# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import urllib

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import base64
import logging
import requests
import json


class partner_inherit(models.Model):
    _inherit = 'res.partner'

    farmer_type = fields.Boolean("Is Farmer")
    farmer_survey_id = fields.Char('Survey ID')
    district = fields.Many2one('res.district', 'District')
    epa = fields.Char('EPA')
    village = fields.Many2one('res.district.village', 'Village', required=False)
    farmer_name = fields.Char("Farmer's Name (First Name and Surname)", required=False)
    farmer_id = fields.Char("Farmer's 180 ID")
    farmer_photo_1 = fields.Binary("Farmer's Photo 1 (Whole body in front of hut)", required=False)
    farmer_photo_2 = fields.Binary("Farmer's Photo 2 (Whole body in front of hut)", required=False)
    farmer_photo_3 = fields.Binary("Farmer's Photo 3 (Whole body ideally next to trees)")
    farmer_photo_4 = fields.Binary("Farmer's Photo 4 (With whole family)")
    farmer_photo_5 = fields.Binary("Farmer's Photo 5 (Clear image of multiple trees of the farmer with whole family)")
    farmer_national_id = fields.Char("Farmer's National ID")
    farmer_age = fields.Integer("Farmer's Age")
    is_married = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string='Married')
    farmer_wife_name = fields.Char("Wife's Name")
    farmer_wife_age = fields.Integer("Wife's Age")
    farmer_children = fields.Integer("No. Of Children")
    no_of_kids_ids = fields.One2many('farmer.kids.details', 'farmer_kids_details_id', string="No. Of Kids")
    farmer_farming_list = fields.Char('What is the farmer farming on his fields? ')
    farmer_fruit_trees = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string='Does the farmer grow fruit trees?')
    farmer_grow_fruit_trees = fields.Char(string='What fruit does the farmer grow?')
    no_of_tres_for_planting = fields.Integer('How many trees would the farmer like to plant?')
    efficient_cook_stove = fields.Selection([('Yes', 'Yes'), ('No', 'No')],
                                            string='Does he have an energy efficient cook-stove??')
    get_firewood_from = fields.Char("Where does the farmer get firewood now? ")
    hours_taken_per_week = fields.Float('How many hours does this take per week?')
    comments = fields.Text('Comments')
    special_info_farmer = fields.Text('Special information about farmer')


class farmer_survey(models.Model):
    _name = 'farmer.survey'
    _rec_name = 'farmer_survey_id'

    farmer_survey_id = fields.Char('Survey ID')
    district = fields.Many2one('res.district', 'District')
    epa = fields.Char('EPA')
    village = fields.Many2one('Village', required=False)
    farmer_name = fields.Char("Farmer's Name (First Name and Surname)", required=False)
    farmer_id = fields.Char("Farmer's 180 ID")
    farmer_photo_1 = fields.Binary("Farmer's Photo 1 (Whole body in front of hut)", required=False)
    farmer_photo_2 = fields.Binary("Farmer's Photo 2 (Whole body in front of hut)", required=False)
    farmer_photo_3 = fields.Binary("Farmer's Photo 3 (Whole body ideally next to trees)")
    farmer_photo_4 = fields.Binary("Farmer's Photo 4 (With whole family)")
    farmer_photo_5 = fields.Binary("Farmer's Photo 5 (Clear image of multiple trees of the farmer with whole family)")
    farmer_national_id = fields.Char("Farmer's National ID")
    farmer_age = fields.Integer("Farmer's Age")
    is_married = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string='Married')
    farmer_wife_name = fields.Char("Wife's Name")
    farmer_wife_age = fields.Integer("Wife's Age")
    farmer_children = fields.Integer("No. Of Children")
    no_of_kids_ids = fields.One2many('farmer.kids.details', 'farmer_kids_details_id', string="No. Of Kids")
    farmer_farming_list = fields.Char('What is the farmer farming on his fields? ')
    farmer_fruit_trees = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string='Does the farmer grow fruit trees?')
    farmer_grow_fruit_trees = fields.Char(string='What fruit does the farmer grow?')
    no_of_tres_for_planting = fields.Integer('How many trees would the farmer like to plant?')
    efficient_cook_stove = fields.Selection([('Yes', 'Yes'), ('No', 'No')],
                                            string='Does he have an energy efficient cook-stove??')
    get_firewood_from = fields.Char("Where does the farmer get firewood now? ")
    hours_taken_per_week = fields.Float('How many hours does this take per week?')
    comments = fields.Text('Comments')
    special_info_farmer = fields.Text('Special information about farmer')

    def get_farmer_survey_details(self):

        # Authentication
        access_token = ''
        url = 'https://www.earth.ff1.co.za/api/v1/User/signin'
        email = 'planetodoo'
        password = 'nG8#dDwes$B*WDP8qku2'
        header = {
            "Content-Type": "application/json"
        }

        body = {
            'Email': email,
            'Password': password
        }

        response = requests.post(url, data=json.dumps(body), headers=header)
        if response.status_code == 200:
            response_text = json.loads(response.text)
            access_token = response_text['d']['token']
        else:
            raise ValidationError(_("There's something wrong! Please check your request again."))

        # Getting & Storing Survey Answers

        phtoto_data_1 = ''

        if access_token:
            answer_url = 'https://www.earth.ff1.co.za/api/v1/Survey/5f0eda300fdfb21193f3f5c4/answer'
            body_data = {
                "paging": {"size": 20, "page": 1},
                "sort": {"_UD": -1},
                "where": {"_UD": {"$gt": "2020-06-01", "$lt": "2020-08-01"}}
            }
            answer_header = {
                "Content-Type": "application/json",
                'Authorization': str(access_token)
            }

            answer_response = requests.get(answer_url, data=json.dumps(body_data), headers=answer_header)
            if answer_response.status_code == 200:
                answer_response_text = json.loads(answer_response.text)
                values = {}
                children_list = []
                survey_id = str(answer_response_text['d']['data'][0]['_id'])
                survey = self.env['farmer.survey'].search([('farmer_survey_id', '=', survey_id)])
                if not survey:

                    # F1 Value
                    district_values = {
                        'district_name': answer_response_text['d']['data'][0]['F1']
                    }

                    district = self.env['res.district'].create(district_values)

                    # F3 Value
                    village_values = {
                        'district_name': district.id,
                        'village_name': answer_response_text['d']['data'][0]['F3']
                    }

                    village = self.env['res.district.village'].create(village_values)

                    p_data_1 = str(answer_response_text['d']['data'][0]['F6'])
                    photo_data_1 = p_data_1.strip('data:image/jpeg;base64,')

                    p_data_2 = str(answer_response_text['d']['data'][0]['F7'])
                    photo_data_2 = p_data_2.strip('data:image/jpeg;base64,')

                    p_data_3 = str(answer_response_text['d']['data'][0]['F8'])
                    photo_data_3 = p_data_3.strip('data:image/jpeg;base64,')

                    p_data_4 = str(answer_response_text['d']['data'][0]['F9'])
                    photo_data_4 = p_data_4.strip('data:image/jpeg;base64,')

                    p_data_5 = str(answer_response_text['d']['data'][0]['F10'])
                    photo_data_5 = p_data_5.strip('data:image/jpeg;base64,')

                    # F20 Value (What is the farmer farming on his fields?)

                    list_of_trees = answer_response_text['d']['data'][0]['F20']

                    values.update({
                        'farmer_survey_id': answer_response_text['d']['data'][0]['_id'],  # Survey ID
                        'district': district.id,
                        'epa': answer_response_text['d']['data'][0]['F2'],
                        'village': village.id,
                        'farmer_name': answer_response_text['d']['data'][0]['F4'],
                        'farmer_id': answer_response_text['d']['data'][0]['F5'],
                        'farmer_photo_1': '/' + photo_data_1,  # F6
                        'farmer_photo_2': '/' + photo_data_2,  # F7
                        'farmer_photo_3': '/' + photo_data_3,  # F8
                        'farmer_photo_4': '/' + photo_data_4,  # F9
                        'farmer_photo_5': '/' + photo_data_5,  # F10
                        'farmer_national_id': answer_response_text['d']['data'][0]['F11'],
                        'farmer_age': int(answer_response_text['d']['data'][0]['F12']),
                        'farmer_wife_name': answer_response_text['d']['data'][0]['F14'],
                        'farmer_wife_age': int(answer_response_text['d']['data'][0]['F15']),
                        'farmer_children': int(answer_response_text['d']['data'][0]['F16']),
                        'no_of_kids_ids': children_list,  # F17 - F19
                        'farmer_farming_list': list_of_trees,  # F20
                        'farmer_grow_fruit_trees': answer_response_text['d']['data'][0]['F22'],  # F22
                        'no_of_tres_for_planting': int(answer_response_text['d']['data'][0]['F23']),
                        'get_firewood_from': answer_response_text['d']['data'][0]['F25'],
                        'hours_taken_per_week': float(answer_response_text['d']['data'][0]['F26']),
                        'comments': answer_response_text['d']['data'][0]['F27'],
                    })

                    #  F13 Value (Is Married?)
                    if answer_response_text['d']['data'][0]['F13'] == 'Married':
                        values.update({'is_married': 'Yes'})
                    else:
                        values.update({'is_married': 'No'})

                    # F17 - F19 Values (No. Of Children)

                    if answer_response_text['d']['data'][0]['F13'] == 'Married':
                        for name in answer_response_text['d']['data'][0]['F17']:
                            for age in answer_response_text['d']['data'][0]['F18']:
                                for gender in answer_response_text['d']['data'][0]['F19']:
                                    children_vals = [(0, 0, {
                                        'farmer_kids_details_id': self.id,
                                        'farmer_kid_name': name,
                                        'farmer_kid_age': age,
                                        'farmer_kid_gender': gender,
                                    })]
                                    values.update({'no_of_kids_ids': children_list})

                    # F21 Value (Does the farmer grow fruit trees?)

                    if answer_response_text['d']['data'][0]['F21'] == 'Yes':
                        values.update({'farmer_fruit_trees': 'Yes'})
                    else:
                        values.update({'farmer_fruit_trees': 'No'})

                    # F24 Value (Does he have an energy efficient cook-stove?)
                    if answer_response_text['d']['data'][0]['F24'] == 'Yes':
                        values.update({'efficient_cook_stove': 'Yes'})
                    else:
                        values.update({'efficient_cook_stove': 'No'})

                    self.update(values)

                    country = self.env['res.country'].search([('id', '=', 155)])
                    values.update({
                        'company_type': 'person',
                        'farmer_type': True,
                        'type': '',
                        'name': answer_response_text['d']['data'][0]['F4'],
                        'country_id': country.id
                    })

                    farmer = self.env['res.partner'].search([('farmer_survey_id', '=', 'farmer_survey_id')], limit=1)
                    if not farmer:
                        farmer.create(values)
            else:
                raise ValidationError(_("There's something wrong! Please check your request again."))


class farmer_kids_details(models.Model):
    _name = 'farmer.kids.details'

    farmer_kids_details_id = fields.Many2one('farmer.survey', "Farmer's Kids ID")
    farmer_kid_name = fields.Char('Name')
    farmer_kid_age = fields.Char('Age')
    farmer_kid_gender = fields.Char('Gender')
