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
    no_of_kids_ids = fields.One2many('farmer.kids.details', 'farmer_kids_details_res_partner_id', string="No. Of Kids")
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
        url = 'http://dms.agrotechltd.org/api/survey-data/search-data'
        username = 'planetodoo'
        password = 'nG8#dDwes$B*WDP8qku2'
        header = {
            "Content-Type": "application/json",
            "username":username,
            "password":password

        }

        body = {
            "_ids": {
                "PId": "5f0ea9f2b92e9cbc41480a7b",
                "SNId": "5fb5128ccf7a2188672b3621",
                "SId": "5fb7501a5b08adb808f18cc0"

            },
            "_page": {"per": 10, "page": 1}

        }

        response = requests.post(url, data=json.dumps(body), headers=header)
        if response.status_code == 200:
            response_text = json.loads(response.text)
        else:
            raise ValidationError(_("There's something wrong! Please check your request again."))

        # Getting & Storing Survey Answers

        phtoto_data_1 = ''

        if response.status_code == 200:
            response_text = json.loads(response.text)
            values = {}
            children_list = []
            survey_id = str(response_text['d'][0]['_id'])
            survey = self.env['farmer.survey'].search([('farmer_survey_id', '=', survey_id)])
            if not survey:
                # F1 Value
                district_values = {
                    'district_name': response_text['d'][0]['district'][0]
                }

                district = self.env['res.district'].create(district_values)

                # F3 Value
                village_values = {
                    'district_name': district.id,
                    'village_name': response_text['d'][0]['village']
                }

                village = self.env['res.district.village'].create(village_values)

                p_data_1 = str(response_text['d'][0]['farmer_photo_1'])
                photo_data_1 = p_data_1.strip('data:image/jpeg;base64,')

                p_data_2 = str(response_text['d'][0]['farmer_photo_2'])
                photo_data_2 = p_data_2.strip('data:image/jpeg;base64,')

                p_data_3 = str(response_text['d'][0]['farmer_photo_3'])
                photo_data_3 = p_data_3.strip('data:image/jpeg;base64,')

                p_data_4 = str(response_text['d'][0]['farmer_photo_4_family'])
                photo_data_4 = p_data_4.strip('data:image/jpeg;base64,')

                p_data_5 = str(response_text['d'][0]['farmer_photo_5_multiple_tree'])
                photo_data_5 = p_data_5.strip('data:image/jpeg;base64,')

                # F20 Value (What is the farmer farming on his fields?)

                list_of_trees = response_text['d'][0]['fruit_farmer_grow'][0]

                country = self.env['res.country'].search([('name', '=', response_text['d'][0]['country'][0])]).id

                values.update({
                    'farmer_survey_id': response_text['d'][0]['_id'],  # Survey ID
                    'district': district.id,
                    'epa': response_text['d'][0]['EPA'][0],
                    'village': village.id,
                    'country_id': country,
                    'farmer_name': response_text['d'][0]['farmer_name'],
                    'farmer_id': response_text['d'][0]['180_farmer_Id'],
                    'farmer_photo_1': '/' + photo_data_1,  # F6
                    'farmer_photo_2': '/' + photo_data_2,  # F7
                    'farmer_photo_3': '/' + photo_data_3,  # F8
                    'farmer_photo_4': '/' + photo_data_4,  # F9
                    'farmer_photo_5': '/' + photo_data_5,  # F10
                    'farmer_national_id': response_text['d'][0]['national_ID'],
                    'farmer_age': int(response_text['d'][0]['age_of_farmer']),
                    'farmer_wife_name': response_text['d'][0]['wife_name'],
                    'farmer_wife_age': int(response_text['d'][0]['wife_age']),
                    'farmer_children': int(response_text['d'][0]['number_of_kids']),
                    'no_of_kids_ids': children_list,  # F17 - F19
                    'farmer_farming_list': list_of_trees,  # F20
                    'farmer_grow_fruit_trees': response_text['d'][0]['farmer_grow_fruit_trees'],  # F22
                    'no_of_tres_for_planting': int(response_text['d'][0]['trees_farmer_would_like_plant']),
                    'get_firewood_from': response_text['d'][0]['source_of_firewood'],
                    'hours_taken_per_week': float(response_text['d'][0]['hours_per_week']),
                    # 'comments': answer_response_text['d'][0]['F27'],
                })

                #  F13 Value (Is Married?)
                if response_text['d'][0]['married'][0] == 'Yes':
                    values.update({'is_married': 'Yes'})
                else:
                    values.update({'is_married': 'No'})

                # F17 - F19 Values (No. Of Children)

                if response_text['d'][0]['married'][0] == 'Yes':
                    for name in response_text['d'][0]['name_of_kid']:
                        pos_tion = response_text['d'][0]['name_of_kid'].index(name)
                        age = response_text['d'][0]['age_of_kid'][pos_tion]
                        gender = response_text['d'][0]['gender_of_kid'][pos_tion][0]
                        # for age in response_text['d'][0]['age_of_kid']:
                        #     for gender in response_text['d'][0]['gender_of_kid']:
                        kids_objs = self.env['farmer.kids.details'].create({
                            'farmer_kids_details_id': self.id,
                            'farmer_kid_name': name,
                            'farmer_kid_age': age,
                            'farmer_kid_gender': gender,
                        })

                # F21 Value (Does the farmer grow fruit trees?)

                if response_text['d'][0]['farmer_grow_fruit_trees'][0] == 'Yes':
                    values.update({'farmer_fruit_trees': 'Yes'})
                else:
                    values.update({'farmer_fruit_trees': 'No'})

                # F24 Value (Does he have an energy efficient cook-stove?)
                if response_text['d'][0]['have_energy_efficient_cookstove'][0] == 'Yes':
                    values.update({'efficient_cook_stove': 'Yes'})
                else:
                    values.update({'efficient_cook_stove': 'No'})

                self.update(values)

                values.update({
                    'company_type': 'person',
                    'farmer_type': True,
                    'type': '',
                    'name': response_text['d'][0]['farmer_name'],
                    'country_id': country
                })

                farmer = self.env['res.partner'].search([('farmer_survey_id', '=', 'farmer_survey_id')], limit=1)
                if not farmer:
                    farmer.create(values)
            else:
                raise ValidationError(_("There's something wrong! Please check your request again."))


class farmer_survey(models.Model):
    _name = 'farmer.survey'
    _rec_name = 'farmer_survey_id'

    farmer_survey_id = fields.Char('Survey ID')
    district = fields.Many2one('res.district', 'District')
    epa = fields.Char('EPA')
    village = fields.Many2one('res.district.village', required=False)
    country_id = fields.Many2one('res.country', "Country")
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
        url = 'http://dms.agrotechltd.org/api/survey-data/search-data'
        username = 'planetodoo'
        password = 'nG8#dDwes$B*WDP8qku2'
        header = {
            "Content-Type": "application/json",
            "username":username,
            "password":password

        }

        body = {
            "_ids": {
                "PId": "5f0ea9f2b92e9cbc41480a7b",
                "SNId": "5fb5128ccf7a2188672b3621",
                "SId": "5fb7501a5b08adb808f18cc0"

            },
            "_page": {"per": 10, "page": 1}

        }

        response = requests.post(url, data=json.dumps(body), headers=header)
        if response.status_code == 200:
            response_text = json.loads(response.text)
            print(response_text)
        else:
            raise ValidationError(_("There's something wrong! Please check your request again."))

        # Getting & Storing Survey Answers

        phtoto_data_1 = ''

        if response.status_code == 200:
            response_text = json.loads(response.text)
            values = {}
            children_list = []
            survey_id = str(response_text['d'][0]['_id'])
            survey = self.env['farmer.survey'].search([('farmer_survey_id', '=', survey_id)])
            print(survey)
            print(survey_id)
            if not survey:
                # F1 Value
                district_values = {
                    'district_name': response_text['d'][0]['district'][0]
                }

                district = self.env['res.district'].create(district_values)

                # F3 Value
                village_values = {
                    'district_name': district.id,
                    'village_name': response_text['d'][0]['village']
                }

                village = self.env['res.district.village'].create(village_values)

                p_data_1 = str(response_text['d'][0]['farmer_photo_1'])
                photo_data_1 = p_data_1.strip('data:image/jpeg;base64,')

                p_data_2 = str(response_text['d'][0]['farmer_photo_2'])
                photo_data_2 = p_data_2.strip('data:image/jpeg;base64,')

                p_data_3 = str(response_text['d'][0]['farmer_photo_3'])
                photo_data_3 = p_data_3.strip('data:image/jpeg;base64,')

                p_data_4 = str(response_text['d'][0]['farmer_photo_4_family'])
                photo_data_4 = p_data_4.strip('data:image/jpeg;base64,')

                p_data_5 = str(response_text['d'][0]['farmer_photo_5_multiple_tree'])
                photo_data_5 = p_data_5.strip('data:image/jpeg;base64,')

                # F20 Value (What is the farmer farming on his fields?)

                list_of_trees = response_text['d'][0]['fruit_farmer_grow'][0]

                country = self.env['res.country'].search([('name', '=', response_text['d'][0]['country'][0])]).id

                values.update({
                    'farmer_survey_id': response_text['d'][0]['_id'],  # Survey ID
                    'district': district.id,
                    'epa': response_text['d'][0]['EPA'][0],
                    'village': village.id,
                    'country_id': country,
                    'farmer_name': response_text['d'][0]['farmer_name'],
                    'farmer_id': response_text['d'][0]['180_farmer_Id'],
                    'farmer_photo_1': '/' + photo_data_1,  # F6
                    'farmer_photo_2': '/' + photo_data_2,  # F7
                    'farmer_photo_3': '/' + photo_data_3,  # F8
                    'farmer_photo_4': '/' + photo_data_4,  # F9
                    'farmer_photo_5': '/' + photo_data_5,  # F10
                    'farmer_national_id': response_text['d'][0]['national_ID'],
                    'farmer_age': int(response_text['d'][0]['age_of_farmer']),
                    'farmer_wife_name': response_text['d'][0]['wife_name'],
                    'farmer_wife_age': int(response_text['d'][0]['wife_age']),
                    'farmer_children': int(response_text['d'][0]['number_of_kids']),
                    'no_of_kids_ids': children_list,  # F17 - F19
                    'farmer_farming_list': list_of_trees,  # F20
                    'farmer_grow_fruit_trees': response_text['d'][0]['farmer_grow_fruit_trees'],  # F22
                    'no_of_tres_for_planting': int(response_text['d'][0]['trees_farmer_would_like_plant']),
                    'get_firewood_from': response_text['d'][0]['source_of_firewood'],
                    'hours_taken_per_week': float(response_text['d'][0]['hours_per_week']),
                    # 'comments': answer_response_text['d'][0]['F27'],
                })

                #  F13 Value (Is Married?)
                if response_text['d'][0]['married'][0] == 'Yes':
                    values.update({'is_married': 'Yes'})
                else:
                    values.update({'is_married': 'No'})

                # F17 - F19 Values (No. Of Children)

                if response_text['d'][0]['married'][0] == 'Yes':
                    for name in response_text['d'][0]['name_of_kid']:
                        pos_tion = response_text['d'][0]['name_of_kid'].index(name)
                        age=response_text['d'][0]['age_of_kid'][pos_tion]
                        gender=response_text['d'][0]['gender_of_kid'][pos_tion][0]
                        # for age in response_text['d'][0]['age_of_kid']:
                        #     for gender in response_text['d'][0]['gender_of_kid']:
                        kids_objs = self.env['farmer.kids.details'].create({
                            'farmer_kids_details_id': self.id,
                            'farmer_kid_name': name,
                            'farmer_kid_age': age,
                            'farmer_kid_gender': gender,
                        })


                # F21 Value (Does the farmer grow fruit trees?)

                if response_text['d'][0]['farmer_grow_fruit_trees'][0] == 'Yes':
                    values.update({'farmer_fruit_trees': 'Yes'})
                else:
                    values.update({'farmer_fruit_trees': 'No'})

                # F24 Value (Does he have an energy efficient cook-stove?)
                if response_text['d'][0]['have_energy_efficient_cookstove'][0] == 'Yes':
                    values.update({'efficient_cook_stove': 'Yes'})
                else:
                    values.update({'efficient_cook_stove': 'No'})

                self.update(values)

                values.update({
                    'company_type': 'person',
                    'farmer_type': True,
                    'type': '',
                    'name': response_text['d'][0]['farmer_name'],
                    'country_id': country
                })

                farmer = self.env['res.partner'].search([('farmer_survey_id', '=', 'farmer_survey_id')])
                if not farmer:
                    part_id = farmer.create(values)
                    no_kids = self.env['farmer.kids.details'].search([('farmer_kids_details_id', '=',self.id)])
                    no_kids.write({'farmer_kids_details_res_partner_id': part_id})
            else:
                raise ValidationError(_("There's something wrong! Please check your request again."))


class farmer_kids_details(models.Model):
    _name = 'farmer.kids.details'

    farmer_kids_details_id = fields.Many2one('farmer.survey', "Farmer's Kids ID")
    farmer_kids_details_res_partner_id = fields.Many2one('res.partner', "Farmer's Kids ID")
    farmer_kid_name = fields.Char('Name')
    farmer_kid_age = fields.Char('Age')
    farmer_kid_gender = fields.Char('Gender')
