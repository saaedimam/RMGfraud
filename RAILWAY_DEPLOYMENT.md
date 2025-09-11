# Railway Deployment Guide for RMGFraud

This guide will help you deploy your Flask application on Railway with a PostgreSQL database.

## 🚀 Quick Start (5 minutes)

### Step 1: Prepare Your Code
```bash
# Make sure all changes are committed
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### Step 2: Deploy to Railway

1. **Go to [railway.app](https://railway.app)**
2. **Sign up/Login** with GitHub
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your RMGfraud repository**
6. **Railway will auto-detect it's a Python app**

### Step 3: Add PostgreSQL Database

1. **In your project dashboard, click "New"**
2. **Select "Database" → "PostgreSQL"**
3. **Railway will create a PostgreSQL database**
4. **Copy the connection string** (you'll need this)

### Step 4: Configure Environment Variables

1. **Go to your service settings**
2. **Click "Variables" tab**
3. **Add these environment variables:**

```
SECRET_KEY=your-very-secure-secret-key-here
DATABASE_URL=postgresql://postgres:password@host:port/railway
FLASK_ENV=production
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=your-admin-password
ENCRYPTION_KEY=your-32-character-encryption-key
WTF_CSRF_ENABLED=true
LOG_LEVEL=INFO
```

### Step 5: Initialize Database

1. **Go to your service**
2. **Click "Deploy Logs"**
3. **Click the "Connect" button** (opens terminal)
4. **Run these commands:**

```bash
# Initialize database tables
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database tables created successfully!')
"

# Create admin user
python create_admin.py
```

### Step 6: Test Your App

1. **Click the generated URL** (e.g., `https://rmgfraud-production.up.railway.app`)
2. **Test the main functionality**
3. **Verify database operations work**
4. **Check authentication flow**

## 🔧 Detailed Configuration

### Environment Variables Explained

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | `your-very-secure-secret-key-here` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@host:port/railway` |
| `FLASK_ENV` | Flask environment | `production` |
| `MAIL_SERVER` | SMTP server for emails | `smtp.gmail.com` |
| `MAIL_USERNAME` | Email username | `your-email@gmail.com` |
| `MAIL_PASSWORD` | Email app password | `your-app-password` |
| `ADMIN_EMAIL` | Admin user email | `admin@yourdomain.com` |
| `ADMIN_PASSWORD` | Admin user password | `your-admin-password` |

### Database Setup

Railway automatically provides:
- ✅ PostgreSQL database
- ✅ Connection string in `DATABASE_URL`
- ✅ Automatic backups
- ✅ Connection pooling

### Custom Domain (Optional)

1. **Go to your service settings**
2. **Click "Domains" tab**
3. **Add your custom domain**
4. **Configure DNS records** as shown

## 📊 Monitoring & Logs

### View Logs
- **Deploy Logs**: Real-time deployment logs
- **Service Logs**: Application runtime logs
- **Metrics**: CPU, memory, and network usage

### Health Checks
- Railway automatically monitors your app
- Restarts if it becomes unresponsive
- Sends notifications for issues

## 🔄 Updates & Maintenance

### Deploy Updates
```bash
# Make your changes
git add .
git commit -m "Update application"
git push origin main

# Railway automatically redeploys
```

### Database Migrations
```bash
# Connect to Railway terminal
# Run migrations
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database updated!')
"
```

## 💰 Pricing

### Free Tier (Hobby Plan)
- ✅ $5 credit monthly
- ✅ 500 hours of usage
- ✅ 1GB RAM
- ✅ 1GB disk space
- ✅ PostgreSQL database included
- ✅ Custom domains
- ✅ Automatic deployments

### Pro Plan ($5/month)
- ✅ Everything in Hobby
- ✅ More resources
- ✅ Priority support
- ✅ Team collaboration

## 🛠️ Troubleshooting

### Common Issues

1. **App won't start:**
   - Check environment variables
   - Verify `DATABASE_URL` is correct
   - Check deploy logs for errors

2. **Database connection issues:**
   - Ensure PostgreSQL service is running
   - Verify `DATABASE_URL` format
   - Check if database is accessible

3. **Static files not loading:**
   - Ensure files are in `static/` directory
   - Check file permissions
   - Verify file paths in templates

4. **Email not working:**
   - Check SMTP credentials
   - Verify `MAIL_*` environment variables
   - Test with a simple email first

### Debug Commands

```bash
# Check if app starts locally
python run.py

# Test database connection
python -c "
from app import app, db
with app.app_context():
    print('Database connected:', db.engine.url)
"

# Check environment variables
python -c "
import os
print('SECRET_KEY:', bool(os.environ.get('SECRET_KEY')))
print('DATABASE_URL:', bool(os.environ.get('DATABASE_URL')))
"
```

## 🔐 Security Best Practices

1. **Use strong secret keys**
2. **Enable HTTPS** (automatic on Railway)
3. **Set secure environment variables**
4. **Regular security updates**
5. **Monitor access logs**

## 📈 Performance Optimization

1. **Enable Gunicorn workers** (already configured)
2. **Use database connection pooling**
3. **Implement caching** for static content
4. **Optimize database queries**
5. **Monitor resource usage**

## 🆘 Support

- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **Community Discord**: [discord.gg/railway](https://discord.gg/railway)
- **GitHub Issues**: For code-related problems

---

## 🎉 You're All Set!

Your RMGFraud application should now be running on Railway with:
- ✅ Automatic deployments from GitHub
- ✅ PostgreSQL database
- ✅ HTTPS enabled
- ✅ Custom domain support
- ✅ Monitoring and logs

**Next Steps:**
1. Test all functionality
2. Set up monitoring alerts
3. Configure custom domain (optional)
4. Set up regular backups
5. Monitor performance and usage
