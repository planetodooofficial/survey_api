
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import base64
import logging
import requests
import json


class Config_Survey(models.Model):
    _name = 'config.survey'
    _rec_name= 'pid'

    pid = fields.Char('project_id')
    snid = fields.Char('SNid')

    farmer_page_count = fields.Integer('Farmer Survey page Count')
    tree_page_count = fields.Integer('Tree Survey page Count')

