from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BookHistory(models.Model):
    _name = "library.book.history"

    book_id = fields.Many2one('library.book')
    user_id = fields.Many2one('res.users')
    old_state = fields.Char(string="Old State")
    new_state = fields.Char(string="New State")
    reason = fields.Char(string="Reason")
    author_ids = fields.One2many('library.author', 'book_his_id')

