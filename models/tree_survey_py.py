# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import base64
import logging
import requests
import json


class tree_survey_py(models.Model):
    _name = 'tree.survey.data'
    _rec_name = 'tree_survey_id'

    tree_name = fields.Char("Tree Name")
    tree_survey_id = fields.Char('Survey ID')
    farmer_name = fields.Many2one('res.partner', "Farmer's Name")
    farmer_id = fields.Char("Farmer's 180 ID", required=False)
    country_id = fields.Many2one('res.country', 'Country')
    gps_location = fields.Char('Location')
    tree_type = fields.Char('Tree Type')
    tree_image_1 = fields.Binary('Image 1', required=False)
    tree_image_2 = fields.Binary('Image 2', required=False)
    tree_image_3 = fields.Binary('Image 3')
    survey_date = fields.Char('Survey Date')

    def get_trees_py_survey_details(self):

        # Authentication
        access_token = ''
        url = 'http://dms.agrotechltd.org/api/survey-data/search-data'
        username = 'planetodoo'
        password = 'nG8#dDwes$B*WDP8qku2'
        header = {
            "Content-Type": "application/json",
            "username": username,
            "password": password

        }

        body = {
            "_ids": {
                "PId": "5f0ea9f2b92e9cbc41480a7b",
                "SNId": "5fb5128ccf7a2188672b3621",
                "SId": "5fb7502eb35e73bd09aab87c"

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
            prod_val = {}
            categ = ''

            for response_text in response_text['d']:
                survey_id = str(response_text['_id'])
                print(response_text['image_of_tree_1'])
                survey = self.env['tree.survey.data'].search([('tree_survey_id', '=', survey_id)])
                if not survey_id == '5f1296be5d082f5b6e04f65f':
                    if not survey:
                        print(response_text['image_of_tree_1'])
                        photo_data_1 = str(response_text['image_of_tree_1'])
                        phtoto_data_1 = photo_data_1.strip('data:image/jpeg;base64,')

                        photo_data_2 = str(response_text['image_of_tree_2'])
                        phtoto_data_2 = photo_data_2.strip('data:image/jpeg;base64,')

                        photo_data_3 = str(response_text['image_of_tree_3'])
                        phtoto_data_3 = photo_data_3.strip('data:image/jpeg;base64,')

                        farmer = self.env['res.partner'].search(
                            [('farmer_id', '=', str(response_text['180_farmer_Id']))])
                        if not farmer:
                            farmer.get_farmer_survey_details()
                            farmer = self.env['res.partner'].search(
                                [('farmer_id', '=', str(response_text['180_farmer_Id']))])
                        values.update({
                            'tree_name': response_text['tree_Id'],
                            'tree_survey_id': response_text['_id'],  # Survey ID
                            'farmer_id': response_text['180_farmer_Id'],
                            'country_id': farmer.country_id.id,
                            'gps_location': response_text['GPS'],
                            'tree_image_1': '/' + phtoto_data_1,
                            'tree_image_2': '/' + phtoto_data_2,
                            'tree_image_3': '/' + phtoto_data_3,
                            'survey_date': response_text['date_capture'],
                            # 'tree_type': response_text['tree_type'],
                        })

                        self.env['tree.survey.data'].create(values)

                        tree = self.env['product.template'].search(
                            [('tree_survey_id', '=', response_text['_id'])], limit=1)
                        route_id = self.env['stock.location.route'].search([('name', '=', 'Dropship')])

                        categ = self.env['product.category'].search(
                            ['|', ('name', '=', farmer.country_id.name), ('name', '=', 'Malawi')])
                        if not categ:
                            val_categ = {}
                            val_categ.update({
                                'name': farmer.country_id.name or 'Malawi',
                                'route_ids': [(6, 0, [route_id.id])]
                            })
                            categ = categ.create(val_categ)

                        if not tree:
                            prod_val.update({
                                'farmer_name': farmer.id,
                                'farmer_id': farmer.farmer_id,
                                'name': response_text['tree_Id'],
                                'type': 'product',
                                'categ_id': categ.id,
                                'route_ids': [(6, 0, [route_id.id])]
                            })

                            product = tree.create(prod_val)

                            seller_val = {
                                'name': farmer.id or 10,
                                'min_qty': 1,
                                'product_uom': product.uom_id.id,
                                'price': product.standard_price,
                                'product_name': product.name,
                                'product_id': self.env['product.product'].search(
                                    [('product_tmpl_id', '=', product.id)]).id,
                                'product_tmpl_id': product.id,
                            }
                            farmer_supplier = self.env['product.supplierinfo'].create(seller_val)
        else:
            raise ValidationError(_("There's something wrong! Please check your request again."))
