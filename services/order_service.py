from odoo import models, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class OrderService(models.Model):
    _name = 'test.order.service'
    _description = 'Order Business Service'

    @api.model
    def create_order(self, data):

        # =========================
        # 1. VALIDATION
        # =========================
        if not data.get('partner_id'):
            raise UserError(_("Customer is required"))

        if not data.get('order_lines'):
            raise UserError(_("At least one product line is required"))

        product_ids = [
            line['product_id']
            for line in data['order_lines']
            if line.get('product_id')
        ]

        # =========================
        # Lock STOCK
        # =========================
        if product_ids:
            self.env.cr.execute("""
                SELECT id
                FROM stock_quant
                WHERE product_id = ANY(%s)
                FOR UPDATE
            """, (product_ids,))

        # =========================
        # 3. STOCK CHECK
        # =========================
        StockQuant = self.env['stock.quant'].sudo()

        for line in data['order_lines']:
            product_id = line.get('product_id')
            qty_requested = float(line.get('quantity', 1.0))

            if not product_id:
                continue


            quants = StockQuant.search([
                ('product_id', '=', product_id),
                ('location_id.usage', '=', 'internal')
            ])

            available_qty = sum(quants.mapped('quantity'))

            product = self.env['product.product'].sudo().browse(product_id)

            _logger.info(
                "LOCK CHECK → Product: %s | Available: %s | Requested: %s",
                product.display_name,
                available_qty,
                qty_requested
            )

            if available_qty < qty_requested:
                raise UserError(_(
                    "Not enough stock for product '%s'. Available: %s, Requested: %s"
                ) % (product.display_name, available_qty, qty_requested))

        # =========================
        # 4. CREATE ORDER (SAFE)
        # =========================
        order = self.env['test.sale.order'].sudo().create({
            'partner_id': data['partner_id'],
            'order_line_ids': [
                (0, 0, {
                    'product_id': line['product_id'],
                    'quantity': line.get('quantity', 1.0),
                })
                for line in data['order_lines']
            ]
        })

        _logger.info("ORDER CREATED SUCCESSFULLY: %s", order.name)

        return order