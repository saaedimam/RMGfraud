#!/bin/bash

# Vercel Deployment Script for RMGFraud
# This script helps you deploy your Flask app to Vercel

echo "🚀 RMGFraud Vercel Deployment Script"
echo "===================================="

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

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

echo "✅ Vercel CLI is ready"

# Check if user is logged in
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please login to Vercel first:"
    vercel login
fi

echo "✅ Vercel authentication ready"

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
echo "This will deploy your Flask app as serverless functions."
echo ""
echo "⚠️  If you get a 'No Next.js version detected' error:"
echo "   1. Go to your Vercel project settings"
echo "   2. Go to 'General' tab"
echo "   3. Set 'Framework Preset' to 'Other'"
echo "   4. Set 'Root Directory' to '.'"
echo "   5. Set 'Build Command' to 'pip install -r requirements.txt'"
echo "   6. Set 'Output Directory' to '.'"
echo ""

vercel

echo ""
echo "🎉 Deployment initiated!"
echo ""
echo "Next steps:"
echo "1. Set up external PostgreSQL database (Supabase, Railway, or Neon)"
echo "2. Add environment variables in Vercel dashboard:"
echo "   - SECRET_KEY"
echo "   - DATABASE_URL"
echo "   - FLASK_ENV=production"
echo "3. Initialize database tables"
echo "4. Create admin user"
echo ""
echo "For detailed instructions, see the README.md deployment section"
