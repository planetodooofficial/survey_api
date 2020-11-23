# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import base64
import logging
import requests
import json


class cook_stove_survey(models.Model):
    _name = 'cook.stove.survey'
    _rec_name = 'cook_stove_survey_id'

    cook_stove_survey_id = fields.Char('Survey Id')
    farmer_id = fields.Char("Farmer's ID")
    t_a = fields.Char('T/A')
    name_of_chief = fields.Char('Name Of Chief')
    name_of_village = fields.Char('Name Of Village')
    type_of_kitchen = fields.Char('Type Of Kitchen', requried=True)
    cooking_method = fields.Char('Cooking Method', requried=True)
    have_an_axe = fields.Selection([('Yes', 'yes'), ('No', 'no')], string='Do you have an axe?', requried=True)
    per_week_walking_for_firewood = fields.Float('How many hours per week walking for firewood?', requried=True)
    stove_id = fields.Char('Stove ID')
    kitchen_gps_location = fields.Char('Kitchen GPS Location', requried=True)
    same_stove_used = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string='Is this the only stove that you use?',
                                       requried=True)
    stove_condition = fields.Selection([('Average', 'avg'), ('Yes', 'Yes'), ('No', 'No')],
                                       string='Is the stove in good condition?')
    comments_1 = fields.Text('Suggestions')
    comments_2 = fields.Text('Extra Suggestions')

    def get_cookstove_survey_details(self):

        # Authentication
        access_token = ''
        url = 'https://earth.ff1.co.za/api/v1/User/signin'
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
            answer_url = 'https://earth.ff1.co.za/api/v1/Survey/5f0f021c0fdfb21193f3f5e8/answer'
            body_data = {
                "paging": {"size": 20, "page": 1},
                "sort": {"_UD": -1},
                "where": {"_UD": {"$gt": "2020-05-01", "$lt": "2020-08-01"}}
            }
            answer_header = {
                "Content-Type": "application/json",
                'Authorization': str(access_token)
            }

            answer_response = requests.get(answer_url, data=json.dumps(body_data), headers=answer_header)
            if answer_response.status_code == 200:
                answer_response_text = json.loads(answer_response.text)
                values = {}

                survey_id = str(answer_response_text['d']['data'][0]['_id'])
                survey = self.env['farmer.survey'].search([('farmer_survey_id', '=', survey_id)])
                if not survey:

                    values.update({
                        'cook_stove_survey_id': answer_response_text['d']['data'][0]['_id'],
                        'farmer_id': answer_response_text['d']['data'][0]['F1'],
                        't_a': answer_response_text['d']['data'][0]['F2'],
                        # 'name_of_chief': answer_response_text['d']['data'][0]['F3'],
                        'name_of_village': answer_response_text['d']['data'][0]['F3'],
                        'type_of_kitchen': answer_response_text['d']['data'][0]['F4'],
                        'cooking_method': answer_response_text['d']['data'][0]['F5'],
                        # 'have_an_axe': answer_response_text['d']['data'][0]['F6'],
                        'per_week_walking_for_firewood': answer_response_text['d']['data'][0]['F7'],
                        'stove_id': answer_response_text['d']['data'][0]['F8'],
                        'kitchen_gps_location': answer_response_text['d']['data'][0]['F9'],
                        'comments_1': answer_response_text['d']['data'][0]['F12'],
                    })


                    # F6 Value (have_an_axe)
                    if answer_response_text['d']['data'][0]['F6'] == True:
                        values.update({'have_an_axe': 'Yes'})
                    else:
                        values.update({'have_an_axe': 'No'})


                    # F12 Value (Is this the only stove that you use?)

                    if answer_response_text['d']['data'][0]['F10'] == True:
                        values.update({'same_stove_used': 'Yes'})
                    else:
                        values.update({'same_stove_used': 'No'})

                    # F13 Value (Is the stove in good condition?)
                    #question ask about average scenerio

                    if answer_response_text['d']['data'][0]['F11'] == 'Average':
                        values.update({'stove_condition': 'avg'})
                    elif answer_response_text['d']['data'][0]['F11'] == 'Yes':
                        values.update({'stove_condition': 'Yes'})
                    else:
                        values.update({'stove_condition': 'No'})

                    self.update(values)
            else:
                raise ValidationError(_("There's something wrong! Please check your request again."))
