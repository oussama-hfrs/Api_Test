from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
import json


class CategoryController(http.Controller):

    """
    Use Case 1 - CRUD simple
    Depends on test test_category model to post and get product categories

    """

    # -------------------------
    # POST CATEGORIES
    # -------------------------
    @http.route('/api/categories', type='http', auth='none', methods=['POST'], csrf=False)
    def create_category(self):
            try:
                data = json.loads(request.httprequest.data)

                # -------------------------
                # HANDLING 400 ERROR
                # -------------------------

                if not data.get('name'):
                    return request.make_json_response(
                        {'error': 'Field "name" is required'},
                        status=400
                    )

                category = request.env['test.category'].sudo().create({
                    'name': data['name']
                })

                return request.make_json_response({
                    'id': category.id,
                    'name': category.name
                }, status=201)

            except Exception as e:
                return request.make_json_response({
                    'error': str(e)
                }, status=500)


    # -------------------------
    # GET CATEGORIES
    # -------------------------
    @http.route('/api/categories', type='http', auth='none', methods=['GET'], csrf=False)
    def list_categories(self):
            categories = request.env['test.category'].sudo().search([])

            data = {
                'categories': [
                    {'id': c.id, 'name': c.name}
                    for c in categories
                ]
            }

            return request.make_json_response(data)


    # -------------------------
    # GET CATEGORIES BY ID
    # -------------------------
    @http.route('/api/categories/<int:category_id>', type='http', auth='none', methods=['GET'], csrf=False)
    def get_category(self, category_id):
        category = request.env['test.category'].sudo().browse(category_id)

        # -------------------------
        # HANDLING 404 ERROR
        # -------------------------

        if not category.exists():
            return  request.make_json_response({
                    'error': 'Category not found'
                }, status=404)
        data = {
            'categories': [
                {'id': c.id, 'name': c.name}
                for c in category
            ]
        }

        return request.make_json_response(data)
