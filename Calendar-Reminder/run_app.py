#!/usr/bin/env python
"""Simple script to run the Flask app"""
import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
