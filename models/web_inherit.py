# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import base64
import logging
import requests
import json


class inherit_web(models.Model):
    _inherit = 'sale.order'

    is_gift= fields.Boolean('Is a gift')
    occasion=fields.Selection([
        ('birth', 'Birthday'),
        ('ani', "anniversary")],string='occasion')
    message=fields.Text('Message')


class inherit_stock(models.Model):
    _inherit = 'stock.picking'

    is_gift= fields.Boolean('Is a gift')
    occasion=fields.Selection([
        ('birth', 'Birthday'),
        ('ani', "anniversary")],string='occasion')
    message=fields.Text('Message')


