from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

class Book(models.Model):
    _name = "library.book"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char(string="Name", required=True, tracking=1)
    ref = fields.Char(default="New")
    year = fields.Integer(string="Year", required=True)
    in_stock = fields.Boolean(string='In Stock')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed')
    ], default='draft')
    author_ids = fields.One2many('library.author', 'book_id')
    author_idss = fields.One2many('author.lines', 'book_id')
    time = fields.Integer(compute='_compute_time')
    assign_to = fields.Many2one('res.partner', string='Partner')
    expected_selling_date = fields.Date(string='Expected Selling Date')
    is_late = fields.Boolean(string='Late')
    # created_date = fields.Date(default=fields.Datetime.now())
    new_date = fields.Datetime(compute='compute_new_date')
    active = fields.Boolean(default=True)


    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Name Should be unique!')
    ]

    @api.constrains('year')
    def year_check(self):
        for rec in self:
            if rec.year <= 1950:
                raise ValidationError("Year Should be greater than 1950")

    # @api.onchange('name')
    # def year_check(self):
    #     for rec in self:
    #         if len(rec.name) > 6:
    #             raise ValidationError("Name Length Should be less than 6")

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super().create(vals_list)
    #     print(vals_list)
    #     return res
    #
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
    #     res = super()._search(domain, offset=0, limit=None, order=None, count=False, access_rights_uid=None)
    #     print(res, '\n', domain)
    #     return res

    def action_state_draft(self):
        for rec in self:
            rec.create_book_history(rec.state, 'draft')
            rec.state = 'draft'

    def action_state_pending(self):
        for rec in self:
            rec.create_book_history(rec.state, 'pending')
            rec.state = 'pending'

    def action_state_sold(self):
        for rec in self:
            rec.create_book_history(rec.state, 'sold')
            rec.state = 'sold'

    def action_state_closed(self):
        for rec in self:
            rec.create_book_history(rec.state, 'closed')
            rec.state = 'closed'

    def action_is_late(self):
        book_ids = self.search([])
        for rec in book_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                print(rec)
                rec.is_late = True

    @api.depends('year')
    def _compute_time(self):
        for rec in self:
            rec.time = 2024 - rec.year


    @api.model
    def create(self, vals_list):
        res = super().create(vals_list)
        if res.ref == "New":
            res.ref = self.env['ir.sequence'].next_by_code('book_sequence')

        return res

    def create_book_history(self, old_state, new_state, reason=''):
        for rec in self:
            rec.env['library.book.history'].create({
                'book_id': rec.id,
                'user_id': rec.env.uid,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or '',
                'author_ids': [(0, 0, {'name': line.name, 'age': line.age}) for line in self.author_ids]
            })


    def action_open_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('library.book_wizard_action')
        action['context'] = {'default_book_id': self.id}
        return action

    def compute_new_date(self):
        self.new_date = self.create_date + datetime.timedelta(hours=6)


class AuthorLines(models.Model):
    _name = 'author.lines'

    author_id = fields.Many2one('library.author')
    book_id = fields.Many2one('library.book')
    name = fields.Char('Name')
    age = fields.Integer('age')
