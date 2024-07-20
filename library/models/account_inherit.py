from odoo import models, fields

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    def action_button(self):
        print(self, "Inside Action_button")