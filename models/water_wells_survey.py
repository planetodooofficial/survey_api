# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import base64
import logging
import requests
import json

class water_well_survey(models.Model):
    _name = 'water.well.survey'
    _rec_name = 'water_well_survey_id'

    water_well_survey_id = fields.Char('Survey ID')
    district = fields.Char('District')
    TA = fields.Char('TA')
    village_name = fields.Char('Village Name')
    first_last_name_chief = fields.Char('First & Last name of Chief')
    date = fields.Date('Date')
    well_gps_location = fields.Char('Well Location Location')
    id_number_well = fields.Char('180 ID Number of well')
    well_image_1 = fields.Binary('Photo of Well')
    well_image_2 = fields.Binary('Photo of well with 180 sticker + pump id number clearly visible')
    well_image_3 = fields.Binary('Photo of well with people using it')
    comments_1 = fields.Text("Comments")
    comments_2 = fields.Text("Comments")

    def get_waterwell_survey_details(self):

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

        if access_token:
            answer_url = 'https://www.earth.ff1.co.za/api/v1/Survey/5f10ad6526caa386aec99d33/answer'
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

                values.update({
                    'water_well_survey_id' : answer_response_text['d']['data'][0]['_id'],
                    'district': answer_response_text['d']['data'][0]['F1'],
                    'TA' : answer_response_text['d']['data'][0]['F2'],
                    'village_name': answer_response_text['d']['data'][0]['F3'],
                    'first_last_name_chief': answer_response_text['d']['data'][0]['F4'],
                    'date': answer_response_text['d']['data'][0]['F5'],
                    'well_gps_location': answer_response_text['d']['data'][0]['F6'],
                    'id_number_well': answer_response_text['d']['data'][0]['F7'],
                    'well_image_1': answer_response_text['d']['data'][0]['F8'],
                    'well_image_2': answer_response_text['d']['data'][0]['F9'],
                    'well_image_3': answer_response_text['d']['data'][0]['F10']
                })

                self.update(values)
            else:
                raise ValidationError(_("There's something wrong! Please check your request again."))

