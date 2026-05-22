"""Database models and shared Flask extensions."""

from datetime import datetime, timezone

from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access that page."
login_manager.login_message_category = "warning"


class User(UserMixin, db.Model):
    """Application user with role-specific seller and delivery metadata."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, index=True)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    vehicle_type = db.Column(db.String(60))
    vehicle_number = db.Column(db.String(40))
    driving_license_number = db.Column(db.String(80))
    verification_status = db.Column(db.String(30))

    store_name = db.Column(db.String(120))
    seller_rating = db.Column(db.Float, nullable=False, default=0.0)
    total_products = db.Column(db.Integer, nullable=False, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def role_label(self):
        labels = {
            "customer": "Customer",
            "seller": "Seller",
            "delivery_agent": "Delivery Agent",
        }
        return labels.get(self.role, "User")

    @property
    def dashboard_endpoint(self):
        endpoints = {
            "customer": "auth.customer_dashboard",
            "seller": "auth.seller_dashboard",
            "delivery_agent": "auth.delivery_dashboard",
        }
        return endpoints.get(self.role, "auth.login")


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
