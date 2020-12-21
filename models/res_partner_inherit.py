from odoo import models, fields, api, _

class ResPartnerInherit(models.Model):
    _inherit='res.partner'

    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], string= 'Gender')

    day = fields.Char('Date')
    month= fields.Char('Month')
    year= fields.Char('Year')

    sale_detail_ids = fields.One2many('website.sale.detail', 'res_partner_id', string='Sale Details')


class WebsiteSaleDetail(models.Model):
    _name= 'website.sale.detail'

    tree_id = fields.Integer(string="Tree Id", related='product_tree_name.id', store= True)
    product_tree_name = fields.Many2one('product.product', string='Tree')
    is_gift = fields.Boolean('Is Gift')
    qty = fields.Integer('Quantity')
    sale_id = fields.Many2one('sale.order','Sale Order')
    payment_id = fields.Many2one('payment.transaction','Transaction Id')

    res_partner_id = fields.Many2one('res.partner', 'Partner_id')