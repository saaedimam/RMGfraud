# Vercel Deployment Guide for RMGFraud

This guide will help you deploy your Flask application on Vercel.

## ⚠️ Important Considerations

**Vercel Limitations:**
- Vercel is designed for serverless functions, not traditional web apps
- Database connections may timeout (10-second limit for hobby plan)
- File uploads are limited to 4.5MB
- No persistent file storage (use external storage like AWS S3)
- SQLite won't work (use PostgreSQL or external database)

## 🚀 Deployment Steps

### 1. Prepare Your Repository

Make sure all files are committed to Git:
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### 2. Set Up External Database

Since Vercel doesn't support persistent databases, you'll need an external PostgreSQL database:

**Option A: Supabase (Recommended - Free tier available)**
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Get your database URL from Settings > Database
4. Format: `postgresql://postgres:[password]@[host]:5432/postgres`

**Option B: Railway**
1. Go to [railway.app](https://railway.app)
2. Create new project > Database > PostgreSQL
3. Get connection string from Variables tab

**Option C: Neon**
1. Go to [neon.tech](https://neon.tech)
2. Create free account and database
3. Get connection string

### 3. Deploy to Vercel

#### Method 1: Vercel CLI (Recommended)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy from your project directory:**
   ```bash
   cd /Users/mac.alvi/Desktop/RMGFraud/RMGfraud
   vercel
   ```

4. **Follow the prompts:**
   - Set up and deploy? `Y`
   - Which scope? (Choose your account)
   - Link to existing project? `N`
   - Project name: `rmgfraud` (or your preferred name)
   - Directory: `./` (current directory)
   - Override settings? `N`

#### Method 2: Vercel Dashboard

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your Git repository
4. Vercel will auto-detect it's a Python project

### 4. Configure Environment Variables

In your Vercel project dashboard:

1. Go to **Settings** > **Environment Variables**
2. Add the following variables:

```
SECRET_KEY=your-very-secure-secret-key-here
DATABASE_URL=postgresql://username:password@host:port/database_name
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

### 5. Initialize Database

After deployment, you need to initialize your database:

1. **SSH into your Vercel function** (if possible) or use a local script
2. **Run database migrations:**
   ```bash
   # Set environment variables locally
   export DATABASE_URL=your_postgresql_url
   export SECRET_KEY=your_secret_key
   
   # Run migrations
   python -c "
   from app import app, db
   with app.app_context():
       db.create_all()
       print('Database initialized successfully!')
   "
   ```

3. **Create admin user:**
   ```bash
   python create_admin.py
   ```

### 6. Test Your Deployment

1. Visit your Vercel URL (e.g., `https://rmgfraud.vercel.app`)
2. Test the main functionality
3. Check if database operations work
4. Verify authentication flow

## 🔧 Troubleshooting

### Common Issues:

1. **Database Connection Timeout:**
   - Use connection pooling
   - Optimize database queries
   - Consider using Vercel Pro for longer timeouts

2. **File Upload Issues:**
   - Files are limited to 4.5MB
   - Use external storage (AWS S3, Cloudinary)
   - Implement file compression

3. **Session Issues:**
   - Sessions may not persist between function calls
   - Consider using external session storage (Redis)

4. **Static Files:**
   - Ensure all static files are in the `static/` directory
   - Vercel will serve them automatically

### Performance Optimization:

1. **Enable Vercel Edge Functions** (if applicable)
2. **Use Vercel's CDN** for static assets
3. **Implement caching** for database queries
4. **Optimize images** and assets

## 📊 Monitoring

1. **Vercel Analytics:** Monitor performance and usage
2. **Function Logs:** Check Vercel dashboard for errors
3. **Database Monitoring:** Use your database provider's dashboard

## 🔄 Updates

To update your deployment:
```bash
git add .
git commit -m "Update application"
git push origin main
# Vercel will automatically redeploy
```

## 💰 Pricing

- **Hobby Plan:** Free (with limitations)
- **Pro Plan:** $20/month (better performance, longer timeouts)
- **Team Plan:** $20/user/month

## 🆘 Support

If you encounter issues:
1. Check Vercel function logs
2. Verify environment variables
3. Test database connectivity
4. Check Vercel documentation
5. Contact Vercel support

---

**Note:** Vercel is not ideal for traditional Flask applications with persistent databases. Consider Railway, Render, or Heroku for better compatibility with your current architecture.
