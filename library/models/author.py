from odoo import models, fields

class Author(models.Model):
    _name = 'library.author'

    name = fields.Char(string="Author", required=True)
    age = fields.Integer(string='Age')
    book_id = fields.Many2one('library.book')
    book_his_id = fields.Many2one('library.book.history')