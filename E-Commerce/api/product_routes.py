"""Product catalog routes for sellers and customers."""

from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user
from sqlalchemy.orm import joinedload

from api.auth_routes import role_required
from database.models import Product, User, db
from utils.helpers import delete_product_image

product_bp = Blueprint("products", __name__)


def get_marketplace_products():
    return (
        Product.query.options(joinedload(Product.seller))
        .order_by(Product.created_at.desc())
        .all()
    )


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


@product_bp.route("/seller/products/<int:product_id>/delete", methods=["POST"])
@role_required("seller")
def delete_product(product_id):
    product = Product.query.filter_by(
        id=product_id,
        seller_id=current_user.id,
    ).first_or_404()

    delete_product_image(current_app.static_folder, product.image_filename)

    db.session.delete(product)
    db.session.commit()

    seller = db.session.get(User, current_user.id)
    if seller:
        seller.total_products = Product.query.filter_by(seller_id=seller.id).count()
        db.session.commit()

    flash("Product deleted successfully.", "success")
    return redirect(url_for("auth.seller_dashboard"))


@product_bp.route("/products")
@role_required("customer")
def customer_products():
    products = get_marketplace_products()
    return render_template(
        "products/customer_catalog.html",
        products=products,
        product_count=len(products),
    )


@product_bp.route("/product/<int:product_id>")
@role_required("customer")
def customer_product_detail(product_id):
    product = (
        Product.query.options(joinedload(Product.seller))
        .filter_by(id=product_id)
        .first_or_404()
    )

    return render_template(
        "products/customer_product_details.html",
        product=product,
        seller=product.seller,
    )
