# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class product_batch_split_wizard(models.TransientModel):
    _name = 'product.batch.split.wizard'

    product_id = fields.Many2one('product.template', 'Product Name', readonly=True, store=True)
    available_qty = fields.Char('Available Quantity', readonly=True, store=True)
    split_qty = fields.Char('Quantity to Split')
    location_id = fields.Many2one('stock.location', 'Location', readonly=True, store=True)

    @api.model
    def default_get(self, fields):
        result = super(product_batch_split_wizard, self).default_get(fields)
        product = self.env['product.template'].browse(self.env.context.get('active_id')).id
        quant = self.env['stock.quant'].search([('product_id', '=', product)])
        result.update({
            'product_id': product,
            'available_qty': quant.inventory_quantity,
            'location_id': quant.location_id
        })
        return result

    @api.model
    def split_into_products(self):
        product = self.env['stock.quant'].search([('product_id', '=', id)], limit=1)
        if product:
            if product.inventory_quantity > self.available_qty:
                pass
