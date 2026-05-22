"""Authentication and role-based dashboard routes."""

import re
from functools import wraps

from flask import Blueprint, flash, redirect, render_template, render_template_string, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from database.models import User, db

auth_bp = Blueprint("auth", __name__)

VALID_ROLES = {"customer", "seller", "delivery_agent"}
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def normalize_email(email):
    return (email or "").strip().lower()


def role_dashboard_url(role):
    endpoints = {
        "customer": "auth.customer_dashboard",
        "seller": "auth.seller_dashboard",
        "delivery_agent": "auth.delivery_dashboard",
    }
    return url_for(endpoints[role])


def validate_registration(form):
    role = form.get("role", "").strip()
    full_name = form.get("full_name", "").strip()
    email = normalize_email(form.get("email"))
    password = form.get("password", "")
    confirm_password = form.get("confirm_password", "")
    phone_number = form.get("phone_number", "").strip()
    address = form.get("address", "").strip()

    errors = []
    if not full_name:
        errors.append("Full name is required.")
    if not EMAIL_PATTERN.match(email):
        errors.append("Enter a valid email address.")
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    if password != confirm_password:
        errors.append("Passwords do not match.")
    if role not in VALID_ROLES:
        errors.append("Choose a valid account role.")
    if not phone_number:
        errors.append("Phone number is required.")
    if not address:
        errors.append("Address is required.")

    if role == "seller" and not form.get("store_name", "").strip():
        errors.append("Store name is required for seller accounts.")

    if role == "delivery_agent":
        delivery_fields = {
            "vehicle_type": "Vehicle type",
            "vehicle_number": "Vehicle number",
            "driving_license_number": "Driving license number",
        }
        for field_name, label in delivery_fields.items():
            if not form.get(field_name, "").strip():
                errors.append(f"{label} is required for delivery agent accounts.")

    duplicate_user = User.query.filter_by(email=email).first()
    if duplicate_user:
        errors.append("An account with this email already exists.")

    return errors


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(*args, **kwargs):
            if current_user.role != role:
                flash("You are not allowed to access that dashboard.", "danger")
                return redirect(role_dashboard_url(current_user.role))
            return view_func(*args, **kwargs)

        return wrapped_view

    return decorator


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(role_dashboard_url(current_user.role))

    if request.method == "POST":
        errors = validate_registration(request.form)
        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template("auth/register.html"), 400

        role = request.form.get("role", "").strip()
        user = User(
            full_name=request.form.get("full_name", "").strip(),
            email=normalize_email(request.form.get("email")),
            role=role,
            phone_number=request.form.get("phone_number", "").strip(),
            address=request.form.get("address", "").strip(),
        )
        user.set_password(request.form.get("password", ""))

        if role == "seller":
            user.store_name = request.form.get("store_name", "").strip()
            user.seller_rating = 0.0
            user.total_products = 0

        if role == "delivery_agent":
            user.vehicle_type = request.form.get("vehicle_type", "").strip()
            user.vehicle_number = request.form.get("vehicle_number", "").strip().upper()
            user.driving_license_number = request.form.get("driving_license_number", "").strip().upper()
            user.verification_status = "Pending"

        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Registration successful. Welcome to your dashboard.", "success")
        return redirect(role_dashboard_url(user.role))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(role_dashboard_url(current_user.role))

    if request.method == "POST":
        email = normalize_email(request.form.get("email"))
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        if not EMAIL_PATTERN.match(email):
            flash("Enter a valid email address.", "danger")
            return render_template("auth/login.html"), 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html"), 401

        login_user(user, remember=remember)
        flash(f"Welcome back, {user.full_name}.", "success")
        return redirect(role_dashboard_url(user.role))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/customer/dashboard")
@role_required("customer")
def customer_dashboard():
    return render_dashboard(
        heading="Customer Dashboard",
        accent="Shop computer hardware, gaming gear, and tech accessories.",
        stats=[
            ("Account Role", current_user.role_label),
            ("Saved Address", current_user.address),
            ("Contact", current_user.phone_number),
        ],
    )


@auth_bp.route("/seller/dashboard")
@role_required("seller")
def seller_dashboard():
    return render_dashboard(
        heading="Seller Dashboard",
        accent=current_user.store_name,
        stats=[
            ("Store Name", current_user.store_name),
            ("Seller Rating", f"{current_user.seller_rating:.1f} / 5"),
            ("Total Products", current_user.total_products),
        ],
    )


@auth_bp.route("/delivery/dashboard")
@role_required("delivery_agent")
def delivery_dashboard():
    return render_dashboard(
        heading="Delivery Dashboard",
        accent=f"{current_user.vehicle_type} - {current_user.vehicle_number}",
        stats=[
            ("Verification", current_user.verification_status),
            ("Vehicle", f"{current_user.vehicle_type} ({current_user.vehicle_number})"),
            ("License", current_user.driving_license_number),
        ],
    )


def render_dashboard(heading, accent, stats):
    return render_template_string(
        """
        {% extends "base.html" %}
        {% block title %}{{ heading }} | E-Commerce{% endblock %}
        {% block content %}
        <section class="auth-shell dashboard-shell">
          <div class="auth-card dashboard-card">
            <span class="eyebrow">Tech Products Marketplace</span>
            <h1>{{ heading }}</h1>
            <p class="auth-subtitle">{{ accent }}</p>
            <div class="dashboard-grid">
              {% for label, value in stats %}
              <div class="dashboard-stat">
                <span>{{ label }}</span>
                <strong>{{ value }}</strong>
              </div>
              {% endfor %}
            </div>
            <div class="dashboard-actions">
              <a class="btn btn-primary" href="{{ url_for('auth.logout') }}">Logout</a>
            </div>
          </div>
        </section>
        {% endblock %}
        """,
        heading=heading,
        accent=accent,
        stats=stats,
    )
