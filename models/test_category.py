from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TestCategory(models.Model):
    _name = 'test.category'
    _description = 'Test Product Category'
    _order = 'name'

    name = fields.Char(string='Name', required=True, index=True)
    active = fields.Boolean(default=True)

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name :
                raise ValidationError(_("Category name is required"))