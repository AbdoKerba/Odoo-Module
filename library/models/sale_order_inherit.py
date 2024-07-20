from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    book_id = fields.Many2one('library.book')