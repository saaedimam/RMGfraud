#!/bin/bash

# Railway Deployment Script for RMGFraud
# This script helps you deploy your Flask app to Railway

echo "🚀 RMGFraud Railway Deployment Script"
echo "======================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if changes are committed
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  You have uncommitted changes. Please commit them first:"
    echo "   git add ."
    echo "   git commit -m 'Your commit message'"
    exit 1
fi

echo "✅ Git repository is clean"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

echo "✅ Railway CLI is ready"

# Deploy to Railway
echo "🚀 Deploying to Railway..."
echo "This will open Railway in your browser to complete the setup."

railway login
railway init
railway up

echo ""
echo "🎉 Deployment initiated!"
echo ""
echo "Next steps:"
echo "1. Add PostgreSQL database in Railway dashboard"
echo "2. Set environment variables (see railway-env-example.txt)"
echo "3. Initialize database tables"
echo "4. Create admin user"
echo ""
echo "For detailed instructions, see RAILWAY_DEPLOYMENT.md"
