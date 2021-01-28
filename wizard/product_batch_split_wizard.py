# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class product_batch_split_wizard(models.TransientModel):
    _name = 'product.batch.split.wizard'

    product_id = fields.Many2one('product.template', 'Product Name', readonly=True, store=True)
    available_qty = fields.Float('Available Quantity', readonly=True, store=True)
    split_qty = fields.Float('Quantity to Split')
    location_id = fields.Many2one('stock.location', 'Source Location', readonly=True, store=True)
    dest_location_id = fields.Many2one('stock.location', 'Destination Location')

    @api.model
    def default_get(self, fields):
        result = super(product_batch_split_wizard, self).default_get(fields)

        user_id=self.env.user

        product = self.env['product.template'].sudo().browse(self.env.context.get('active_id')).id
        product_product_id = self.env['product.product'].search([("product_tmpl_id", "=", product)])
        # prod_test=self.env['stock.quant'].sudo().search([('product_id', '=', 51), ('location_id', '=', 30)])
        # print(prod_test)
        location = self.env['stock.location'].sudo().search([('name', '=', 'Stock'), ('company_id','=',user_id.company_id.id)], limit=1).id
        quant = self.env['stock.quant'].sudo().search([('product_id', '=', product_product_id.id), ('location_id', '=', location)])

        result.update({
            'product_id': product,
            'available_qty': quant.quantity,
            'location_id': quant.location_id.id,
            'dest_location_id': quant.location_id.id
        })

        return result



    @api.onchange('split_qty')
    def qty_check(self):
        for qty in self:
            if qty.split_qty > qty.available_qty:
                raise ValidationError(_("Please enter correct quantity for Split. Split Quantity cannot be more than Available Quantity."))



    def split_into_products(self):
        product_product_id = self.env['product.product'].search([("product_tmpl_id", "=", self.product_id.id)])
        product = self.env['stock.quant'].sudo().search([('product_id', '=',product_product_id.id)], limit=1)

        if product:
            product_id = ''
            if int(product.quantity) >= int(self.available_qty):
                loop_counter = self.split_qty
                start_counter = 1
                counter = 1
                while int(start_counter) <= int(loop_counter):
                    values = {
                        'name': 'MALAVI - Dedza' + str(product_product_id.name) + str(counter),
                        'sale_ok': True,
                        'type': 'product',
                        'default_code': 'MALAVI - Dedza' + str(product_product_id.name) + str(counter),
                    }
                    product_id = self.env['product.template'].sudo().create(values)
                    start_counter += 1
                    counter += 1

                    qty_values = {
                        'product_id': product_id.product_variant_id.id,
                        'location_id': self.dest_location_id.id,
                        'inventory_quantity': 1,
                        'quantity': 1,
                        'product_uom_id': product_id.uom_id.id
                    }

                    quantity = self.env['stock.quant'].sudo().create(qty_values)

                quant = self.env['stock.quant'].sudo().search([('product_id', '=', product_product_id.id)])
                if quant:
                    new_qty = product.quantity - self.split_qty

                    remaining_qty = {
                        'inventory_quantity': new_qty,
                        'quantity': new_qty,
                    }

                    remaining_quantity = quant.update(remaining_qty)

                # vals = {
                #     'name': vendor.id,
                #     'min_qty': min_qty,
                #     'product_uom': product_uom.id if product_uom else False,
                #     'price': price,
                #     'product_tmpl_id': old_id_search.product_tmpl_id.id,
                #     'product_id': old_id_search.id
                # }
