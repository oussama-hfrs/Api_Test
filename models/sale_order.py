from odoo import models, fields, api, _
from odoo.exceptions import UserError

class TestSaleOrder(models.Model):
    _name = 'test.sale.order'
    _description = 'Test Sale Order'

    name = fields.Char(default='New', readonly=True, copy=False)
    partner_id = fields.Many2one('res.partner', required=True, string="Customer")
    # -------------------------
    # ORDER LINES
    # -------------------------
    order_line_ids = fields.One2many('test.sale.order.line', 'order_id', string="Lines")
    ref = fields.Char(default='New', readonly=True)
    state = fields.Selection([
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], default='created', tracking=True)

    # -------------------------
    # CURRENCY
    # -------------------------
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id
    )

    total_amount = fields.Monetary(
        compute='_compute_total',
        store=True,
        currency_field='currency_id'
    )


    # -------------------------
    # TOTAL CALCULATION
    # -------------------------

    @api.depends('order_line_ids.price_subtotal')
    def _compute_total(self):
        for order in self:
            order.total_amount = sum(line.price_subtotal for line in order.order_line_ids)

# =========================================================
# ORDER LINE MODEL
# =========================================================

class TestSaleOrderLine(models.Model):
    _name = 'test.sale.order.line'

    order_id = fields.Many2one('test.sale.order', ondelete='cascade')
    product_id = fields.Many2one('product.product', required=True)
    quantity = fields.Float(default=1.0, required=True)
    price_unit = fields.Float(related='product_id.lst_price', readonly=True)
    price_subtotal = fields.Monetary(compute='_compute_subtotal',
                                     store=True,
                                     currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id
    )



    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price_unit