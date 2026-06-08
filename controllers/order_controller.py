from odoo import http
from odoo.http import request
import json
class OrderController(http.Controller):
    """
        Use Case 2 - Logique métier
        Depends on test sale_order and order_service models to create an order to buy several products
    """

    @http.route('/api/orders', type='json', auth='none', methods=['POST'], csrf=False)
    def create_order(self):
        data = json.loads(request.httprequest.data)
        order = request.env['test.order.service'].create_order(data)

        return {
                    'id': order.id,
                    'total_amount': order.total_amount,
                    'state': order.state
                }