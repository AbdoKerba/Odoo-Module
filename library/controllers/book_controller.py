from odoo import http
from odoo.http import request
import json

class BookController(http.Controller):

    # @http.route('/book_controller', methods=['GET'], type='http', auth='none', csrf=False)
    # def get_book_controller(self):
    #     print('hello')

    @http.route('/book_controller', methods=['POST'], type='http', auth='none', csrf=False)
    def book_controller(self):
        args = request.httprequest.data.decode()
        print(args)
        vals = json.loads(args)
        print(vals)

        try:
            rec = request.env['library.book'].sudo().create(vals)
            if rec:
                return request.make_json_response({
                    'message': 'Book Created Successfully.',
                    'id': rec.id,
                    'name': rec.name,
                    'year': rec.year

                }, status=201)
        except Exception as error:
            return request.make_json_response({
                'Error': error
            }, status=500)
