F"""Application entry point for the tech-products e-commerce platform."""

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from config import Config
from database.models import db, login_manager, User, Product


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    login_manager.init_app(app)

    from api.auth_routes import auth_bp
    from api.product_routes import product_bp
    from api.routes import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for("auth.login"))

    @app.route("/dashboard")
    def dashboard_redirect():
        if current_user.is_authenticated:
            return redirect(url_for(current_user.dashboard_endpoint))
        return redirect(url_for("auth.login"))
    
    @app.route('/seller/add-product', methods=['GET', 'POST'])
    @login_required
    def add_product():
        
        if current_user.role != 'seller':
            flash('Access denied.', 'danger')
            return redirect(url_for('dashboard'))

        if request.method == 'POST':

            product_name = request.form.get('product_name')
            category = request.form.get('category')
            specifications = request.form.get('specifications')
            price = request.form.get('price')
            discount = request.form.get('discount')
            return_policy = request.form.get('return_policy')
            shipping_policy = request.form.get('shipping_policy')

            print("\n========== NEW PRODUCT ==========")
            print("Product Name:", product_name)
            print("Category:", category)
            print("Specifications:", specifications)
            print("Price:", price)
            print("Discount:", discount)
            print("Return Policy:", return_policy)
            print("Shipping Policy:", shipping_policy)
            print("=================================\n")
            new_product = Product(
                product_name=product_name,
                category=category,
                specifications=specifications,
                price=float(price),
                discount=float(discount) if discount else 0.0,
                return_policy=return_policy,
                shipping_policy=shipping_policy,
                seller_id=current_user.id
            )
            db.session.add(new_product)
            db.session.commit()
            current_user.total_products = Product.query.filter_by(
                seller_id=current_user.id
            ).count()
            db.session.commit()
            flash('Product uploaded successfully!', 'success')
            return redirect(url_for('auth.seller_dashboard'))

        return render_template('products/add_product.html')

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
