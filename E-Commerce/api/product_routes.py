"""Product catalog routes for sellers."""

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from api.auth_routes import role_required
from database.models import Product

product_bp = Blueprint("products", __name__)


@product_bp.route("/seller/products/<int:product_id>")
@role_required("seller")
def seller_product_detail(product_id):
    product = Product.query.filter_by(
        id=product_id,
        seller_id=current_user.id,
    ).first_or_404()

    return render_template(
        "products/product_details.html",
        product=product,
        seller=current_user,
    )
