from odoo import api, fields, models

class ScrapInherit(models.Model):
    _inherit= 'stock.scrap'

    @api.model
    def default_get(self, fields):
        res = super(ScrapInherit, self).default_get(fields)

        if self._context.get('is_wizard') == 'True':

            product = self.env['product.template'].browse(self.env.context.get("active_id"))
            prod_prod = self.env['product.product'].search([('product_tmpl_id', '=', product.id)])

            res.update({'product_id': prod_prod.id})

            return res

        else:
            return res



