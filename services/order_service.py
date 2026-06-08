from odoo import models, api, _
from odoo.exceptions import UserError

class OrderService(models.Model):
    """
       Business Service Layer:
       - Contains all business rules
       - Called by controllers

    """

    _name = 'test.order.service'
    _description = 'Order Business Service'

    @api.model
    def create_order(self, data):
        # -------------------------
        # 1. VALIDATION RULES
        # -------------------------
        if not data.get('partner_id'):
            raise UserError(_("Customer is required"))
        if not data.get('order_lines') or len(data['order_lines']) == 0:
            raise UserError(_("At least one product line is required"))
        lines = data.get('order_lines')
        print(lines)
        product = self.env['product.product'].browse(lines['product_id'])
        product = product.with_context(lock=True)
        if product.qty_available < lines.quantity:
           raise UserError(f"Insufficient stock for {product.name}")

        # -------------------------
        # 2. BUILD ORDER LINES AND CREATE ORDERS
        # -------------------------
        order = self.env['test.sale.order'].sudo().create({
            'partner_id': data['partner_id'],
            'order_line_ids': [(0, 0, {
                'product_id': line['product_id'],
                'quantity': line.get('quantity', 1.0)
            }) for line in data['order_lines']]
        })
        return order