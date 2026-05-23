"""Main application routes."""

from flask import Blueprint, render_template
from flask_login import current_user

from api.product_routes import get_marketplace_products

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated and current_user.role == "customer":
        products = get_marketplace_products()
        return render_template(
            "products/customer_catalog.html",
            products=products,
            product_count=len(products),
        )

    return render_template("index.html")
