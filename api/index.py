"""
Vercel serverless function entry point for RMGFraud Flask app
"""
import os
import sys
from pathlib import Path

# Add the parent directory to Python path to import app
sys.path.append(str(Path(__file__).parent.parent))

from app import app

def handler(request):
    """Vercel serverless function handler"""
    return app(request.environ, lambda *args: None)
