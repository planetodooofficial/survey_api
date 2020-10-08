# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class products_batch_split(models.Model):
    _inherit = 'product.template'

    unique_id = fields.Char('Product ID')
    stages = fields.Selection([('nursery', 'Nursery'), ('planted', 'Planted'), ('mto', 'MTO')], string='Stages')

