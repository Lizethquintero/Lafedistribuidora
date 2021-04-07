from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"
    
    invima_code = fields.Char('Código Invima', relared="product_id.x_invima")
