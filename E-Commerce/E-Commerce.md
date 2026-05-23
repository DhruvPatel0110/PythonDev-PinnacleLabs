# E-Commerce Shopping Cart System
## Tech Accessories & Computer Parts Marketplace

---

# Project Overview

This project is a Python-based E-Commerce Shopping Cart platform focused entirely on:

- CPU Parts
- GPUs
- RAM Modules
- SSDs / HDDs
- Gaming Accessories
- Keyboards & Mice
- Monitors
- Cooling Systems
- Laptop Accessories
- Tech Gadgets

The platform supports two user roles:

1. Customer
2. Seller

The system allows:
- Product management
- Purchasing
- Cart and wishlist
- Role-based dashboards

---

# Recommended Tech Stack

## Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Optional
- React.js (Only if comfortable)

---

## Backend
- Python
- Flask Framework

### Why Flask?
- Lightweight
- Easy routing
- Beginner friendly
- Faster development

---

## Database
- SQLite (Recommended for internship project)

### Optional
- MySQL

---

# Required Python Libraries

## Flask Libraries

```bash
pip install flask
pip install flask_sqlalchemy
pip install flask_login
pip install flask_wtf
```

---

## Utility Libraries

```bash
pip install pillow
pip install werkzeug
```

---

# Website Theme

## Theme Style

The website revolves entirely around:

- Computer Hardware
- Gaming Components
- Tech Accessories
- Electronic Devices

---

## Suggested Design Theme

### Colors
- Black
- Dark Gray
- Electric Blue
- Neon Green

### Fonts
- Poppins
- Orbitron
- Montserrat

---

# User Roles

---

# 1. CUSTOMER MODULE

## Features

### Customer Registration/Login

Customers can:
- Create account
- Login securely
- Update profile

---

## Customer Dashboard

The dashboard displays:

### Product Listings

Products uploaded by sellers including:
- Product Image
- Product Name
- Seller Name
- Price
- Discount %
- Final Discounted Price
- Product Category
- Product Description
- Stock Availability

---

## Search & Filter System

Customers can filter products based on:
- CPU Parts
- GPUs
- RAM
- SSD
- Accessories
- Price Range
- Brand

---

## Shopping Cart

Customers can:
- Add items to cart
- Remove products
- Update quantity
- View total amount

---

## Checkout Section

Customer enters:
- Full Name
- Delivery Address
- Phone Number
- Pincode
- Payment Method

---

## Order Tracking

Customers can view:
- Order ID
- Delivery Agent Name
- Delivery Agent Contact
- Order Status
- Estimated Delivery Date

---

# 2. SELLER MODULE

## Features

### Seller Registration/Login

Sellers can:
- Create seller account
- Login securely
- Manage profile

---

## Seller Dashboard

Dashboard includes:

### Current Active Listings

Products currently available for sale.

Displayed Data:
- Product Name
- Quantity
- Price
- Discount
- Available Stock

---

## Sold Products Section

Displays:
- Sold Items
- Buyer Name
- Order ID
- Sale Date
- Revenue Earned

---

## Delivery In Progress Section

Shows:
- Orders currently being delivered
- Delivery Agent Assigned
- Customer Details
- Delivery Status

---

## Add New Product

Seller can add:
- Product Name
- Product Image
- Description
- Price
- Discount
- Stock Quantity
- Product Category

---

## Discount Management

Seller can:
- Add discounts
- Edit discounts
- Remove discounts

---

# 3. DELIVERY AGENT MODULE

## Registration Requirements

Before approval, delivery agents must submit:

### Vehicle Details
- Vehicle Type
- Vehicle Number
- Vehicle Model

### Driving License Verification
- License Number
- License Image Upload

---

## Delivery Agent Dashboard

Displays:

### Assigned Orders

Each order includes:
- Order ID
- Seller Address
- Customer Address
- Product Details
- Delivery Status

---

## Order Management

Delivery agent can:
- Accept delivery
- Mark as picked up
- Mark as delivered

---

## Live Order Information

Delivery agents receive:
- Seller Contact
- Customer Contact
- Delivery Instructions

---

# BILLING SYSTEM

## Invoice Generation

An invoice is automatically generated after successful checkout.

---

# Invoice Includes

## Order Information
- Order ID
- Order Date
- Payment Status

---

## Customer Information
- Customer Name
- Customer Address
- Customer Phone

---

## Seller Information
- Seller Name
- Seller Contact
- Seller Address

---

## Delivery Agent Information

(This information is visible to BOTH seller and customer)

- Delivery Agent Name
- Vehicle Number
- Contact Number

---

## Product Information
- Product Name
- Quantity
- Unit Price
- Discount Applied
- Final Amount

---

## Final Billing
- Subtotal
- Delivery Charges
- Tax Amount
- Grand Total

---

# Suggested Database Tables

## Users Table

Stores:
- User ID
- Username
- Email
- Password
- Role

---

## Products Table

Stores:
- Product ID
- Seller ID
- Product Name
- Price
- Discount
- Stock
- Category
- Description

---

## Orders Table

Stores:
- Order ID
- Customer ID
- Seller ID
- Delivery Agent ID
- Order Date
- Delivery Status

---

## Cart Table

Stores:
- Cart ID
- Customer ID
- Product ID
- Quantity

---

## Delivery Agents Table

Stores:
- Vehicle Details
- License Details
- Verification Status

---

# Suggested Folder Structure

```plaintext
ecommerce-project/
│
├── app.py
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── database/
├── models/
├── routes/
├── uploads/
└── invoices/
```

---

# Suggested Website Pages

## Common Pages
- Home Page
- Login Page
- Register Page
- About Us
- Contact Us

---

## Customer Pages
- Customer Dashboard
- Product Details
- Cart Page
- Checkout Page
- Orders Page

---

## Seller Pages
- Seller Dashboard
- Add Product Page
- Manage Products Page
- Sales Analytics Page

---

## Delivery Agent Pages
- Verification Page
- Assigned Deliveries Page
- Delivery Status Page

---

# Security Features

## Recommended Security
- Password Hashing
- Session Management
- Role-Based Access
- File Upload Validation

---

# Future Improvements

Possible upgrades:
- Razorpay/Stripe Integration
- Live GPS Tracking
- AI Product Recommendations
- Chat System
- Email Notifications
- Wishlist Feature
- Product Reviews & Ratings

---

# Recommended Development Plan

## Phase 1
- Setup Flask Project
- Create Database
- Create Login/Register System

---

## Phase 2
- Create Customer Dashboard
- Product Listing System
- Shopping Cart

---

## Phase 3
- Seller Dashboard
- Product Upload System
- Discount Features

---

## Phase 4
- Delivery Agent System
- Billing System
- Invoice Generation

---

# Final Goal

Build a beginner-friendly but realistic E-Commerce platform focused on computer hardware and tech accessories with:

- Multi-role authentication
- Product management
- Order tracking
- Delivery workflow
- Automated invoice generation
- Modern UI design

---

# Skills Demonstrated Through This Project

- Full Stack Development
- Database Management
- Authentication System
- Role-Based Access Control
- CRUD Operations
- Order Processing Workflow
- Invoice Generation
- Real-World Application Logic