from odoo import http , http

class BookController(http.Controller):

    @http.route('/book_controller', methods=['GET'], type='http', auth='none', csrf=False)
    def book_controller(self):
        print('hello')