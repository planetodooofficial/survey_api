# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import base64
import logging
import requests
import json


class tree_survey(models.Model):
    _name = 'tree.survey'
    _rec_name = 'tree_survey_id'

    tree_survey_id = fields.Char('Survey ID')
    scanned_farmer_id = fields.Char("Scanned Farmer's ID", required=True)
    gps_location = fields.Char('Location')
    tree_type = fields.Char('Tree Type')
    tree_image_1 = fields.Binary('Image 1', required=True)
    tree_image_2 = fields.Binary('Image 2', required=True)
    tree_image_3 = fields.Binary('Image 3')
    survey_date = fields.Char('Survey Date')

    def get_trees_survey_details(self):

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
            answer_url = 'https://www.earth.ff1.co.za/api/v1/Survey/5f0efbf60fdfb21193f3f5d9/answer'
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

                values.update({
                    'tree_survey_id': answer_response_text['d']['data'][0]['_id'],  # Survey ID
                    'scanned_farmer_id': answer_response_text['d']['data'][0]['F4'],
                    'gps_location': answer_response_text['d']['data'][0]['F11'],
                    'tree_image_1': answer_response_text['d']['data'][0]['F12'],
                    'tree_image_2': answer_response_text['d']['data'][0]['F13'],
                    'tree_image_3': answer_response_text['d']['data'][0]['F14'],
                    'survey_date': answer_response_text['d']['data'][0]['_UD'],
                })
                self.update(values)
            else:
                raise ValidationError(_("There's something wrong! Please check your request again."))

