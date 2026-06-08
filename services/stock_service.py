from odoo import models, _
from odoo.exceptions import UserError

class StockService(models.Model):
    _name = "test.stock.service"
    _description = "Stock Service"

    def _reserve_stock(self):
        """Prevent overselling with row-level locking"""
        self.ensure_one()
        for line in self.order_line_ids:
            product = line.product_id.with_context(lock=True)  # or use SQL FOR UPDATE
            if product.qty_available < line.quantity:
                raise UserError(f"Insufficient stock for {product.name}")
        # In real life: create stock.move with reservation