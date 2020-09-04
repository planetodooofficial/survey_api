# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class district(models.Model):
    _name = 'res.district'
    _rec_name = 'district_name'

    district_name = fields.Char('District Name')


class district_village(models.Model):
    _name = 'res.district.village'
    _rec_name = 'village_name'

    district_name = fields.Many2one('res.district', 'District Name')
    village_name = fields.Char('Village Name')
