from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import requests
import json


class ApiCallWizard(models.TransientModel):
    _name = 'api.wizard'



    def get_farmer_survey_details(self):

        # Authentication
        access_token = ''
        url = 'http://dms.agrotechltd.org/api/survey/filter'

        cur_user = self.env.user

        # username = 'planetodoo'
        # password = 'nG8#dDwes$B*WDP8qku2'

        username = cur_user.api_user
        password = cur_user.api_pwd

        if not username or not password:
            raise UserError(_("Please Enter API Credentials for your User."))

        header = {
            "Content-Type": "application/json",
            "username": username,
            "password": password

        }
        body_survey = self.env['config.survey'].search([])
        body = {
            "PId": str(body_survey.pid),
            "SNId": str(body_survey.snid),
        }

        # body = {
        #     "_ids": {
        #         "PId": "5f0ea9f2b92e9cbc41480a7b",
        #         "SNId": "5fb5128ccf7a2188672b3621",
        #         "SId": "5fb7501a5b08adb808f18cc0"
        #
        #     },
        #     "_page": {"per": 10, "page": 1}
        #
        # }

        response_filter = requests.post(url, data=json.dumps(body), headers=header)
        if response_filter.status_code == 200:
            response_text = json.loads(response_filter.text)
            print(response_text)
        else:
            raise ValidationError(_("There's something wrong! Please check your request again."))

        # Getting & Storing Survey Answers

        phtoto_data_1 = ''
        sid = ''
        for dict_item in response_text['d']:
            if dict_item['TName'] == "FARMER":
                sid = dict_item['_id']
        print(sid)


        if sid:
            data_url = 'http://dms.agrotechltd.org/api/survey-data/search-data'

            body_data = {
                "_ids": {
                    "PId": str(body_survey.pid),
                    "SNId": str(body_survey.snid),
                    "SId": str(sid)
                },
                "_page": {"per": 10, "page": 1}

            }
            response = requests.post(data_url, data=json.dumps(body_data), headers=header)

            if response.status_code == 200:
                response_text = json.loads(response.text)

                page_count = response_text['Total']

                self.get_farmer_data(body_survey.pid, body_survey.snid, sid, page_count)



    def get_farmer_data(self, pid, snid, sid, page_count):

        cur_user = self.env.user

        username = cur_user.api_user
        password = cur_user.api_pwd

        header = {
            "Content-Type": "application/json",
            "username": username,
            "password": password

        }

        body_survey = self.env['config.survey'].search([])

        if sid:
            for count in range (1, page_count):
                data_url = 'http://dms.agrotechltd.org/api/survey-data/search-data'

                body_data = {
                    "_ids": {
                        "PId": str(body_survey.pid),
                        "SNId": str(body_survey.snid),
                        "SId": str(sid)
                    },
                    "_page": {"per": 10, "page": count}

                }
                response = requests.post(data_url, data=json.dumps(body_data), headers=header)

                if response.status_code == 200:
                    response_text = json.loads(response.text)



                for farm in response_text['d']:
                    values = {}
                    children_list = []
                    survey_id = str(farm['_id'])
                    survey = self.env['farmer.survey'].search([('farmer_survey_id', '=', survey_id)])
                    if not survey:
                        # F1 Value
                        district_values = {
                            # 'district_name': response_text['d'][0]['district'][0]
                            'district_name': farm['district'][0]
                        }

                        district = self.env['res.district'].create(district_values)

                        # F3 Value
                        village_values = {
                            'district_name': district.id,
                            'village_name': farm['location'][0]
                        }

                        village = self.env['res.district.village'].create(village_values)

                        p_data_1 = str(farm['farmer_photo_1'])
                        photo_data_1 = p_data_1.strip('data:image/jpeg;base64,')

                        p_data_2 = str(farm['farmer_photo_2'])
                        photo_data_2 = p_data_2.strip('data:image/jpeg;base64,')

                        p_data_3 = str(farm['farmer_photo_3_family'])
                        photo_data_3 = p_data_3.strip('data:image/jpeg;base64,')

                        p_data_4 = str(farm['farmer_photo_4_family'])
                        photo_data_4 = p_data_4.strip('data:image/jpeg;base64,')


                        # F20 Value (What is the farmer farming on his fields?)

                        list_of_trees = ''
                        for tree  in farm['farming_on_fields']:
                            list_of_trees += tree +','


                        country = self.env['res.country'].search([('name', '=', farm['country'][0])]).id

                        wife_age = farm['wife_age']
                        husband_age = farm['husband_age']

                        values.update({
                            'farmer_survey_id': farm['_id'],  # Survey ID
                            'district': district.id,
                            'village': village.id,
                            'country_id': country,
                            'farmer_name': farm['farmer_name'] +' '+ farm['farmer_last_name'],
                            'farmer_id': farm['180_farmer_Id'],
                            'farmer_photo_1': '/' + photo_data_1,  # F6
                            'farmer_photo_2': '/' + photo_data_2,  # F7
                            'farmer_photo_3': '/' + photo_data_3,  # F8
                            'farmer_photo_4': '/' + photo_data_4,  # F9

                            'farmer_gender': farm['farmer_gender'][0],
                            'farmer_wife_name': farm['wife_name'],
                            'farmer_wife_age': wife_age if wife_age else 0,
                            'farmer_husband_name': farm['husband_first_name'],
                            'farmer_husband_age': husband_age if husband_age else 0,

                            'farmer_national_id': farm['national_ID'],
                            'farmer_age': int(farm['age_of_farmer']),
                            'farmer_children': int(farm['number_of_kids']),
                            'no_of_kids_ids': children_list,  # F17 - F19
                            'farmer_farming_list': list_of_trees,  # F20

                            'farmer_grow_fruit_trees': farm['farmer_grow_fruit_trees'],  # F22
                            'no_of_tres_for_planting': int(farm['trees_farmer_would_like_plant']),
                            'get_firewood_from': farm['source_of_firewood'],
                            'hours_taken_per_week': float(farm['hours_per_week']),

                            # 'comments': answer_response_text['d'][0]['F27'],
                        })

                        #  F13 Value (Is Married?)
                        if farm['marital_status'][0] == 'Married':
                            values.update({'is_married': 'Yes'})
                        else:
                            values.update({'is_married': 'No'})

                        # F17 - F19 Values (No. Of Children)

                        # if response_text['d'][0]['married'][0] == 'Yes':
                        #     for name in response_text['d'][0]['name_of_kid']:
                        #         pos_tion = response_text['d'][0]['name_of_kid'].index(name)
                        #         age = response_text['d'][0]['age_of_kid'][pos_tion]
                        #         gender = response_text['d'][0]['gender_of_kid'][pos_tion][0]
                        #         # for age in response_text['d'][0]['age_of_kid']:
                        #         #     for gender in response_text['d'][0]['gender_of_kid']:
                        #         kids_objs = self.env['farmer.kids.details'].create({
                        #             'farmer_kids_details_id': self.id,
                        #             'farmer_kid_name': name,
                        #             'farmer_kid_age': age,
                        #             'farmer_kid_gender': gender,
                        #         })

                        # F21 Value (Does the farmer grow fruit trees?)

                        if farm['farmer_grow_fruit_trees'][0] == 'Yes':
                            values.update({'farmer_fruit_trees': 'Yes'})
                        else:
                            values.update({'farmer_fruit_trees': 'No'})

                        # F24 Value (Does he have an energy efficient cook-stove?)
                        if farm['have_energy_efficient_cookstove'][0] == 'Yes':
                            values.update({'efficient_cook_stove': 'Yes'})
                        else:
                            values.update({'efficient_cook_stove': 'No'})

                        # self.update(values)
                        farmer_obj_id= self.env['farmer.survey'].create(values)

                        for name in farm['name_of_kid']:
                            if name:
                                pos_tion = farm['name_of_kid'].index(name)
                                age = farm['age_of_kid'][pos_tion]
                                gender = farm['gender_of_kid'][pos_tion][0]
                                # for age in response_text['d'][0]['age_of_kid']:
                                #     for gender in response_text['d'][0]['gender_of_kid']:
                                kids_objs = self.env['farmer.kids.details'].create({
                                    'farmer_kids_details_id': farmer_obj_id.id,
                                    'farmer_kid_name': name,
                                    'farmer_kid_age': age,
                                    'farmer_kid_gender': gender,
                                })

                        values.update({
                            'company_type': 'person',
                            'farmer_type': True,
                            'type': '',
                            'name': farm['farmer_name'],
                            'country_id': country,
                            'image_1920': '/' + photo_data_1,
                            'survey_id': farmer_obj_id.id,
                        })

                        farmer = self.env['res.partner'].search([('farmer_survey_id', '=', 'farmer_survey_id')])
                        if not farmer:
                            part_id = farmer.create(values)
                            no_kids = self.env['farmer.kids.details'].search([('farmer_kids_details_id', '=', farmer_obj_id.id)])
                            no_kids.write({'farmer_kids_details_res_partner_id': part_id})
                    # else:
                    #     raise ValidationError(_("No new records to Import"))








    def get_trees_survey_details(self):

        # Authentication
        access_token = ''
        url = 'http://dms.agrotechltd.org/api/survey/filter'
        # username = 'planetodoo'
        # password = 'nG8#dDwes$B*WDP8qku2'

        cur_user = self.env.user
        cr = self.env.cr

        username = cur_user.api_user
        password = cur_user.api_pwd

        if not username or not password:
            raise UserError(_("Please Enter API Credentials for your User."))

        header = {
            "Content-Type": "application/json",
            "username": username,
            "password": password

        }
        body_survey = self.env['config.survey'].search([])

        body = {
            "PId": str(body_survey.pid),
            "SNId": str(body_survey.snid),
        }

        response_filter = requests.post(url, data=json.dumps(body), headers=header)
        if response_filter.status_code == 200:
            response_text = json.loads(response_filter.text)
            print(response_text)
            print("First API Call")
        else:
            raise ValidationError(_("There's something wrong! Please check your request again."))

        # Getting & Storing Survey Answers

        phtoto_data_1 = ''
        sid = ''
        for dict_item in response_text['d']:
            if dict_item['TName'] == "TREE":
                sid = dict_item['_id']
        print(sid)

        if sid:
            data_url = 'http://dms.agrotechltd.org/api/survey-data/search-data'

            body_data = {
                "_ids": {
                    "PId": str(body_survey.pid),
                    "SNId": str(body_survey.snid),
                    "SId": str(sid)
                },
                "_page": {"per": 10, "page": 1}

            }
            response = requests.post(data_url, data=json.dumps(body_data), headers=header)

            if response.status_code == 200:
                response_text = json.loads(response.text)
                print("Second API Call")

                page_count = response_text['Count']

                self.get_tree_data(body_survey.pid, body_survey.snid, sid, page_count)



    def get_tree_data(self, pid, snid, sid, page_count):

        cur_user = self.env.user

        username = cur_user.api_user
        password = cur_user.api_pwd

        header = {
            "Content-Type": "application/json",
            "username": username,
            "password": password

        }

        body_survey = self.env['config.survey'].search([])

        if sid:
            for count in range (1, page_count):
                data_url = 'http://dms.agrotechltd.org/api/survey-data/search-data'

                body_data = {
                    "_ids": {
                        "PId": str(body_survey.pid),
                        "SNId": str(body_survey.snid),
                        "SId": str(sid)
                    },
                    "_page": {"per": 10, "page": count}

                }
                response = requests.post(data_url, data=json.dumps(body_data), headers=header)

                if response.status_code == 200:
                    response_text = json.loads(response.text)
                    print("Second API Call")


                    values = {}
                    prod_val = {}
                    categ = ''

                    for response_text in response_text['d']:
                        survey_id = str(response_text['_id'])
                        # print(response_text['image_of_tree_1'])
                        survey = self.env['tree.survey'].search([('tree_survey_id', '=', survey_id)])
                        # if not survey_id == '5f1296be5d082f5b6e04f65f':
                        if not survey:
                            photo_data_1 = str(response_text['image_of_tree_1'])
                            phtoto_data_1 = photo_data_1.strip('data:image/jpeg;base64,')

                            photo_data_2 = str(response_text['image_of_tree_2'])
                            phtoto_data_2 = photo_data_2.strip('data:image/jpeg;base64,')

                            # photo_data_3 = str(response_text['image_of_tree_3'])
                            # phtoto_data_3 = photo_data_3.strip('data:image/jpeg;base64,')

                            farmer = self.env['res.partner'].search(
                                [('farmer_id', '=', str(response_text['180_farmer_Id']))])

                            loc = response_text['GPS']

                            location = ",".join([str(i) for i in loc])

                            if not farmer:
                                farmer.get_farmer_survey_details()
                                farmer = self.env['res.partner'].search(
                                    [('farmer_id', '=', str(response_text['180_farmer_Id']))])

                            values.update({
                                'tree_name': response_text['tree_name'][0],
                                'tree_survey_id': response_text['_id'],  # Survey ID
                                'farmer_id': response_text['180_farmer_Id'],
                                'farmer_partner_id': farmer.id,
                                'country_id': farmer.country_id.id,
                                'gps_location': response_text['GPS'],
                                'tree_image_1': '/' + phtoto_data_1,
                                'tree_image_2': '/' + phtoto_data_2,
                                # 'tree_image_3': '/' + phtoto_data_3,
                                # 'survey_date': response_text['date_capture'],
                                # 'tree_type': response_text['tree_type'][0],
                            })

                            # self.write(values)
                            new_tree_survey_obj = self.env['tree.survey'].create(values)

                            tree = self.env['product.template'].search(
                                [('tree_survey_id', '=', response_text['_id'])], limit=1)
                            route_id = self.env['stock.location.route'].search([('name', '=', 'Buy')])

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
                                    'farmer_name': farmer.id or False,
                                    'farmer_id': farmer.farmer_id,
                                    'name': response_text['tree_name'][0],
                                    'type': 'product',
                                    'categ_id': categ.id,
                                    'route_ids': [(6, 0, [route_id.id])],
                                    'image_1920': '/' + phtoto_data_1,
                                    'survey_id': new_tree_survey_obj.id,
                                })

                                prod_val.update(values)

                                product = tree.create(prod_val)

                                # seller_val = {
                                #     'name': farmer.id or 10,
                                #     'min_qty': 1,
                                #     'product_uom': product.uom_id.id,
                                #     'price': product.standard_price,
                                #     'product_name': product.name,
                                #     'product_id': self.env['product.product'].search(
                                #         [('product_tmpl_id', '=', product.id)]).id,
                                #     'product_tmpl_id': product.id,
                                # }
                                # farmer_supplier = self.env['product.supplierinfo'].create(seller_val)


                                # lst = []
                                #
                                # vals = (0, 0, {
                                #     'name': farmer.id or False,
                                #     'min_qty': 1,
                                #     'product_uom': product.uom_id.id,
                                #     'price': product.standard_price,
                                #     'product_name': product.name,
                                #     'product_tmpl_id': product.id,
                                # })
                                #
                                # lst.append(vals)
                                #
                                # product.write({'seller_ids': lst})


                                location = self.env['stock.location'].search([('name', '=', 'Stock')])



                                self.env.cr.commit()

                                # self.env['stock.quant'].with_context(inventory_mode=True).create({
                                #     'product_id': product.id,
                                #     'location_id': location.id,
                                #     'lot_id': False,
                                #     'inventory_quantity': 1,
                                # })
        else:
            raise ValidationError(_("There's something wrong! Please check your request again."))
        return True







    def get_cookstove_survey_details(self):

        # Authentication
        access_token = ''
        url = 'https://earth.ff1.co.za/api/v1/User/signin'
        # email = 'planetodoo'
        # password = 'nG8#dDwes$B*WDP8qku2'

        cur_user = self.env.user

        username = cur_user.api_user
        password = cur_user.api_pwd

        if not username or not password:
            raise UserError(_("Please Enter API Credentials for your User."))

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








    def get_waterwell_survey_details(self):

        # Authentication
        access_token = ''
        url = 'https://earth.ff1.co.za/api/v1/User/signin'
        # email = 'planetodoo'
        # password = 'nG8#dDwes$B*WDP8qku2'

        cur_user = self.env.user

        username = cur_user.api_user
        password = cur_user.api_pwd

        if not username or not password:
            raise UserError(_("Please Enter API Credentials for your User."))

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
            answer_url = 'https://earth.ff1.co.za/api/v1/Survey/5f10ad6526caa386aec99d33/answer'
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

                well_data_1 = answer_response_text['d']['data'][0]['F8']
                img_1 = well_data_1.strip('data:image/jpeg;base64,')

                well_data_2 = answer_response_text['d']['data'][0]['F9']
                img_2 = well_data_2.strip('data:image/jpeg;base64,')

                well_data_3 = answer_response_text['d']['data'][0]['F10']
                img_3 = well_data_3.strip('data:image/jpeg;base64,')

                survey_id = str(answer_response_text['d']['data'][0]['_id'])
                survey = self.env['farmer.survey'].search([('farmer_survey_id', '=', survey_id)])
                if not survey:
                    values.update({
                        'water_well_survey_id': answer_response_text['d']['data'][0]['_id'],
                        'district': answer_response_text['d']['data'][0]['F1'],
                        'TA': answer_response_text['d']['data'][0]['F2'],
                        'village_name': answer_response_text['d']['data'][0]['F3'],
                        'first_last_name_chief': answer_response_text['d']['data'][0]['F4'],
                        'date': answer_response_text['d']['data'][0]['F5'],
                        'well_gps_location': answer_response_text['d']['data'][0]['F6'],
                        'id_number_well': answer_response_text['d']['data'][0]['F7'],
                        'well_image_1': '/' + img_1,
                        'well_image_2': '/' + img_2,
                        'well_image_3': '/' + img_3
                    })

                    self.update(values)
            else:
                raise ValidationError(_("There's something wrong! Please check your request again."))