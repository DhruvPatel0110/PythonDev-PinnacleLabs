"""Shopping cart routes for customers."""

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy.orm import joinedload

from api.auth_routes import role_required
from database.models import CartItem, Product, db

cart_bp = Blueprint("cart", __name__)


def _is_ajax_request():
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def _cart_items_query():
    return (
        CartItem.query.filter_by(user_id=current_user.id)
        .options(
            joinedload(CartItem.product).joinedload(Product.seller),
        )
        .order_by(CartItem.created_at.desc())
    )


@cart_bp.route("/cart")
@role_required("customer")
def view_cart():
    cart_items = _cart_items_query().all()
    cart_total = round(sum(item.subtotal for item in cart_items), 2)
    return render_template(
        "cart/cart.html",
        cart_items=cart_items,
        cart_total=cart_total,
    )


@cart_bp.route("/cart/add/<int:product_id>", methods=["POST"])
@role_required("customer")
def add_to_cart(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        message = "Product not found."
        if _is_ajax_request():
            return jsonify(success=False, message=message, category="danger"), 404
        flash(message, "danger")
        return redirect(url_for("main.index"))

    item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id,
    ).first()

    if item:
        item.quantity += 1
    else:
        db.session.add(
            CartItem(
                user_id=current_user.id,
                product_id=product_id,
                quantity=1,
            )
        )

    db.session.commit()
    message = "Item added to cart"
    if _is_ajax_request():
        return jsonify(success=True, message=message, category="success")

    flash(message, "success")
    return redirect(
        url_for("products.customer_product_detail", product_id=product_id)
    )


@cart_bp.route("/cart/remove/<int:item_id>", methods=["POST"])
@role_required("customer")
def remove_from_cart(item_id):
    item = CartItem.query.filter_by(
        id=item_id,
        user_id=current_user.id,
    ).first_or_404()

    product_name = item.product.product_name if item.product else "Item"
    db.session.delete(item)
    db.session.commit()
    flash(f'"{product_name}" removed from your cart.', "success")
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/cart/update/<int:item_id>", methods=["POST"])
@role_required("customer")
def update_cart_quantity(item_id):
    item = CartItem.query.filter_by(
        id=item_id,
        user_id=current_user.id,
    ).first_or_404()

    try:
        quantity = int(request.form.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        flash("Quantity must be at least 1.", "warning")
        return redirect(url_for("cart.view_cart"))

    item.quantity = quantity
    db.session.commit()
    flash("Cart quantity updated.", "success")
    return redirect(url_for("cart.view_cart"))
