from odoo import models, fields, api, _


class ProductPrices(models.Model):
    _name = 'product.prices'

    name = fields.Char('Name')
    price = fields.Float('Price')