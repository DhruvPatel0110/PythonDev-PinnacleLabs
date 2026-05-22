"""Application entry point for the tech-products e-commerce platform."""

from flask import Flask, redirect, url_for
from flask_login import current_user

from config import Config
from database.models import db, login_manager


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    login_manager.init_app(app)

    from api.auth_routes import auth_bp
    from api.routes import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for("auth.login"))

    @app.route("/dashboard")
    def dashboard_redirect():
        if current_user.is_authenticated:
            return redirect(url_for(current_user.dashboard_endpoint))
        return redirect(url_for("auth.login"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
