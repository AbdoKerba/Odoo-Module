from odoo import models, fields


class ChangeBookState(models.TransientModel):
    _name = 'library.book.state'

    book_id = fields.Many2one('library.book')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending')
    ], default='draft')
    reason = fields.Char('Reason', required='1')

    def action_confirm(self):
        if self.book_id.state == 'closed':
            self.book_id.state = self.state
            self.book_id.create_book_history('closed', self.state, self.reason)