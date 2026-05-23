"""Wishlist routes for customers."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy.orm import joinedload

from api.auth_routes import role_required
from database.models import CartItem, Product, WishlistItem, db

wishlist_bp = Blueprint("wishlist", __name__)


def _wishlist_items_query():
    return (
        WishlistItem.query.filter_by(user_id=current_user.id)
        .options(
            joinedload(WishlistItem.product).joinedload(Product.seller),
        )
        .order_by(WishlistItem.created_at.desc())
    )


@wishlist_bp.route("/wishlist")
@role_required("customer")
def view_wishlist():
    wishlist_items = _wishlist_items_query().all()
    return render_template(
        "user/wishlist.html",
        wishlist_items=wishlist_items,
    )


@wishlist_bp.route("/wishlist/add/<int:product_id>", methods=["POST"])
@role_required("customer")
def add_to_wishlist(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for("main.index"))

    existing = WishlistItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id,
    ).first()

    if existing:
        flash(f'"{product.product_name}" is already in your wishlist.', "info")
    else:
        db.session.add(
            WishlistItem(
                user_id=current_user.id,
                product_id=product_id,
            )
        )
        db.session.commit()
        flash(f'"{product.product_name}" added to your wishlist.', "success")

    return redirect(request.form.get("next") or request.referrer or url_for("wishlist.view_wishlist"))


@wishlist_bp.route("/wishlist/remove/<int:item_id>", methods=["POST"])
@role_required("customer")
def remove_from_wishlist(item_id):
    item = WishlistItem.query.filter_by(
        id=item_id,
        user_id=current_user.id,
    ).first_or_404()

    product_name = item.product.product_name if item.product else "Item"
    db.session.delete(item)
    db.session.commit()
    flash(f'"{product_name}" removed from your wishlist.', "success")
    return redirect(url_for("wishlist.view_wishlist"))


@wishlist_bp.route("/wishlist/move-to-cart/<int:item_id>", methods=["POST"])
@role_required("customer")
def move_to_cart(item_id):
    item = WishlistItem.query.filter_by(
        id=item_id,
        user_id=current_user.id,
    ).first_or_404()

    product = item.product
    if not product:
        db.session.delete(item)
        db.session.commit()
        flash("Product no longer available.", "danger")
        return redirect(url_for("wishlist.view_wishlist"))

    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product.id,
    ).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        db.session.add(
            CartItem(
                user_id=current_user.id,
                product_id=product.id,
                quantity=1,
            )
        )

    db.session.delete(item)
    db.session.commit()
    flash(f'"{product.product_name}" moved to your cart.', "success")
    return redirect(url_for("cart.view_cart"))
