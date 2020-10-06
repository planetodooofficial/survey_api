# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class products_batch_split(models.Model):
    _inherit = 'product.template'

    unique_id = fields.Char('Product ID')
    stages = fields.Selection([('scrap', 'Scrap'), ('nursery', 'Nursery'), ('grown', 'Grown')], string='Stages')

    @api.model
    def split_into_products(self):
        view = self.env.ref('survey_api.product_batch_split_wizard')

        return {
            'name': _('Product Batch Split.'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.batch.split.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': self.env.context,
        }