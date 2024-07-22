from odoo import http
from odoo.http import request
from urllib.parse import parse_qs
import json


class BookController(http.Controller):

    # @http.route('/book_controller', methods=['GET'], type='http', auth='none', csrf=False)
    # def get_book_controller(self):
    #     print('hello')

    @http.route('/book_controller', methods=['POST'], type='http', auth='none', csrf=False)
    def book_controller_create(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get('name'):
            return request.make_json_response({
                'Error': 'Name is required!'})
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

    @http.route('/get_book/<int:book_id>', methods=['GET'], type='http', auth='none', csrf=False)
    def book_controller_get(self, book_id):
        try:
            book_rec = request.env['library.book'].search([('id', '=', book_id)])
            if not book_rec:
                return request.make_json_response({
                    'Error': "ID doesn't exist!"
                }, status=400)
            if book_rec:
                return request.make_json_response({
                    'message': 'Valid Operation',
                    'id': book_rec.id,
                    'name': book_rec.name,
                    'year': book_rec.year

                }, status=200)
        except Exception as error:
            return request.make_json_response({
                'Error': error
            }, status=500)

    @http.route('/get_books', methods=['GET'], type='http', auth='none', csrf=False)
    def book_controller_get_list(self):
        try:
            domain = []
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            if params:
                for key, value in params.items():
                    domain.append((key, '=', value[0]))
            book_ids = request.env['library.book'].search(domain)
            if not book_ids:
                return request.make_json_response({
                    'Error': "There is no books!"
                }, status=400)
            if book_ids:
                return request.make_json_response({
                    'message': 'Valid Operation',
                    'data': [{
                    'id': book_id.id,
                    'name': book_id.name,
                    'year': book_id.year
                } for book_id in book_ids]
                }, status=200)
        except Exception as error:
            return request.make_json_response({
                'Error': error
            }, status=500)

    @http.route('/delete_book/<int:book_id>', methods=['DELETE'], type='http', auth='none', csrf=False)
    def book_controller_delete(self, book_id):
        try:
            book_id = request.env['library.book'].search([('id', '=', book_id)])
            if not book_id:
                return request.make_json_response({
                    'Error': "There is no book with this ID !"
                }, status=400)
            if book_id:
                book_id.unlink()
                return request.make_json_response({
                    'message': 'Book deleted successfully.',
                }, status=200)
        except Exception as error:
            return request.make_json_response({
                'Error': error
            }, status=500)

    @http.route('/book/controller', type='json', methods=['POST'], auth='none', csrf=False)
    def book_controller_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        print(vals)
        try:
            rec = request.env['library.book'].sudo().create(vals)
            if rec:
                return [{'Message': 'Book Created Successfully.',
                         'id': rec.id,
                         'name': rec.name,
                         'year': rec.year}]
        except Exception as error:
            return [{'Error': error}]

