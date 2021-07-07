from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
from odoo import http


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/cart'], type='http', auth="public", website=True)
    def cart(self, **post):
        response = super(WebsiteSale, self).cart(**post)
        order = response.qcontext.get('website_sale_order')
        if order:
            products = order.remove_product_ids.mapped('product_id')
            if products:
                response.qcontext.update(
                    products2remove=[product.with_context(
                        display_default_code=False).display_name for product in products]
                )
                order.remove_product_ids.unlink()
        return response
