"""
Vercel serverless function entry point for RMGFraud Flask app
"""
import os
import sys
from pathlib import Path

# Add the root directory to Python path to import app
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Change working directory to root
os.chdir(root_dir)

from app_vercel import app

def handler(request):
    """Vercel serverless function handler"""
    return app(request.environ, lambda *args: None)
