#!/usr/bin/env python3
"""
RMGFraud Application Runner
Simple script to run the Flask application
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Set environment variables
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('FLASK_DEBUG', '1')
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', '1') == '1'
    )
