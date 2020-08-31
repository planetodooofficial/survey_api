# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import base64
import logging
import requests
import json


class inherit_product(models.Model):
    _inherit = 'product.template'

    tree_name = fields.Char('Tree Name')
    tree_survey_id = fields.Char('Survey ID')
    farmer_name = fields.Many2one('res.partner', "Farmer's Name")
    farmer_id = fields.Char("Farmer's 180 ID")
    country_id = fields.Many2one('res.country', 'Country')
    gps_location = fields.Char('Location')
    tree_type = fields.Char('Tree Type')
    tree_image_1 = fields.Binary('Image 1', required=False)
    tree_image_2 = fields.Binary('Image 2', required=False)
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
                category_id = ''

                for answer_response_text in answer_response_text['d']['data']:
                    survey_id = str(answer_response_text['_id'])
                    survey = self.env['product.template'].search([('tree_survey_id', '=', survey_id)])
                    if not survey_id == '5f1296be5d082f5b6e04f65f':
                        if not survey:
                            photo_data_1 = str(answer_response_text['F12'])
                            phtoto_data_1 = photo_data_1.strip('data:image/jpeg;base64,')

                            photo_data_2 = str(answer_response_text['F13'])
                            phtoto_data_2 = photo_data_2.strip('data:image/jpeg;base64,')

                            photo_data_3 = str(answer_response_text['F14'])
                            phtoto_data_3 = photo_data_3.strip('data:image/jpeg;base64,')

                            values.update({
                                'tree_name': answer_response_text['TreeId'],
                                'tree_survey_id': answer_response_text['_id'],  # Survey ID
                                'gps_location': answer_response_text['F11'],
                                'tree_image_1': '/' + phtoto_data_1,
                                'tree_image_2': '/' + phtoto_data_2,
                                'tree_image_3': '/' + phtoto_data_3,
                                'survey_date': answer_response_text['_UD'],
                            })

                            farmer = self.env['res.partner'].search(
                                [('farmer_id', '=', str(answer_response_text['F4']))])
                            if not farmer:
                                farmer.get_farmer_survey_details()
                                farmer = self.env['res.partner'].search(
                                    [('farmer_id', '=', str(answer_response_text['F4']))])

                            tree = self.env['product.template'].search(
                                [('tree_survey_id', '=', answer_response_text['_id'])], limit=1)
                            route_id = self.env['stock.location.route'].search([('name', '=', 'Dropship')])

                            categ = self.env['product.category'].search([('name', '=', farmer.country_id.name)])
                            if not categ:
                                val_categ = {}
                                val_categ.update({
                                    'name': farmer.country_id.name or 'Malawi',
                                    'route_ids': [(6, 0, [route_id.id])]
                                })
                                categ = categ.create(val_categ)

                            if not tree:
                                values.update({
                                    'farmer_name': farmer.id,
                                    'farmer_id': farmer.farmer_id,
                                    'name': answer_response_text['TreeId'],
                                    'type': 'product',
                                    'categ_id': categ.id,
                                    'route_ids': [(6, 0, [route_id.id])]
                                })

                                product = tree.create(values)

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


class tree_survey(models.Model):
    _name = 'tree.survey'
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
                category_id = ''

                for answer_response_text in answer_response_text['d']['data']:
                    survey_id = str(answer_response_text['_id'])
                    survey = self.env['product.template'].search([('tree_survey_id', '=', survey_id)])
                    if not survey_id == '5f1296be5d082f5b6e04f65f':
                        if not survey:
                            photo_data_1 = str(answer_response_text['F12'])
                            phtoto_data_1 = photo_data_1.strip('data:image/jpeg;base64,')

                            photo_data_2 = str(answer_response_text['F13'])
                            phtoto_data_2 = photo_data_2.strip('data:image/jpeg;base64,')

                            photo_data_3 = str(answer_response_text['F14'])
                            phtoto_data_3 = photo_data_3.strip('data:image/jpeg;base64,')

                            values.update({
                                'tree_name': answer_response_text['TreeId'],
                                'tree_survey_id': answer_response_text['_id'],  # Survey ID
                                'gps_location': answer_response_text['F11'],
                                'tree_image_1': '/' + phtoto_data_1,
                                'tree_image_2': '/' + phtoto_data_2,
                                'tree_image_3': '/' + phtoto_data_3,
                                'survey_date': answer_response_text['_UD'],
                            })

                            farmer = self.env['res.partner'].search(
                                [('farmer_id', '=', str(answer_response_text['F4']))])
                            if not farmer:
                                farmer.get_farmer_survey_details()
                                farmer = self.env['res.partner'].search(
                                    [('farmer_id', '=', str(answer_response_text['F4']))])

                            tree = self.env['product.template'].search(
                                [('tree_survey_id', '=', answer_response_text['_id'])], limit=1)
                            route_id = self.env['stock.location.route'].search([('name', '=', 'Dropship')])

                            categ = self.env['product.category'].search([('name', '=', farmer.country_id.name)])
                            if not categ:
                                val_categ = {}
                                val_categ.update({
                                    'name': farmer.country_id.name or 'Malawi',
                                    'route_ids': [(6, 0, [route_id.id])]
                                })
                                categ = categ.create(val_categ)

                            if not tree:
                                values.update({
                                    'farmer_name': farmer.id,
                                    'farmer_id': farmer.farmer_id,
                                    'name': answer_response_text['TreeId'],
                                    'type': 'product',
                                    'categ_id': categ.id,
                                    'route_ids': [(6, 0, [route_id.id])]
                                })

                                product = tree.create(values)

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
