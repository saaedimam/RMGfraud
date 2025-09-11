# RMGFraud - Fraud Detection Platform

A secure, minimalist, and user-contributed platform dedicated to identifying and addressing fraud within the Ready-Made Garment (RMG) industry.

## 🚀 Features

### Core Functionality
- **Comprehensive Database**: Searchable and filterable entity database with detailed profiles
- **Anonymous Reporting**: Secure, encrypted fraud reporting system for whistleblowers
- **Country Profiles**: Visual analytics and fraud statistics by country
- **Interactive Heatmap**: Global fraud visualization with risk indicators
- **Real-time Search**: Advanced search with multiple filters and sorting options

### Security Features
- **Multi-Factor Authentication (MFA)**: TOTP-based 2FA for enhanced security
- **Role-Based Access Control**: Admin, moderator, and user roles with appropriate permissions
- **End-to-End Encryption**: Secure data transmission and storage
- **Audit Logging**: Comprehensive activity tracking for compliance
- **Secure Authentication**: BGMEA, RMG Supplier, and banking partner verification

### User Interface
- **Dark Theme**: Professional, minimalist design with excellent readability
- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Interactive Visualizations**: Charts, graphs, and maps for data analysis
- **Intuitive Navigation**: Dashboard-style layout with clear information hierarchy

## 🛠️ Technology Stack

- **Backend**: Python Flask with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: Flask-Login with MFA support
- **Security**: Werkzeug security, CSRF protection, secure headers
- **Visualization**: Chart.js, Leaflet.js for maps
- **Styling**: Custom CSS with CSS variables for theming

## 📋 Prerequisites

- Python 3.11+
- pip (Python package installer)
- PostgreSQL (for production)
- Git

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd RMGfraud
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp config.py .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Create admin user**
   ```bash
   python create_admin.py
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///rmgfraud.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Database Configuration

For production, use PostgreSQL:

```env
DATABASE_URL=postgresql://username:password@localhost/rmgfraud
```

## 📁 Project Structure

```
RMGfraud/
├── app.py                 # Main application file
├── config.py             # Configuration settings
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── routes/               # Route blueprints
│   ├── auth.py          # Authentication routes
│   ├── dashboard.py     # Dashboard routes
│   ├── database.py      # Database routes
│   ├── reporting.py     # Reporting routes
│   └── country.py       # Country profile routes
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Homepage
│   ├── auth/            # Authentication templates
│   ├── database/        # Database templates
│   ├── reporting/       # Reporting templates
│   └── country/         # Country templates
├── static/              # Static assets
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── images/         # Images and icons
└── migrations/          # Database migrations
```

## 🔐 Security Features

### Authentication & Authorization
- Multi-factor authentication with TOTP
- Role-based access control (Admin, Moderator, User)
- Secure password hashing with bcrypt
- Session management with secure cookies

### Data Protection
- CSRF protection on all forms
- Input sanitization and validation
- SQL injection prevention with ORM
- XSS protection with content escaping

### Security Headers
- Content Security Policy (CSP)
- HTTP Strict Transport Security (HSTS)
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff

## 📊 Database Schema

### Core Tables
- **Users**: User accounts with authentication and roles
- **Entities**: Companies, individuals, suppliers, manufacturers
- **FraudReports**: Fraud incident reports with evidence
- **CountryProfiles**: Country-level fraud statistics
- **AuditLogs**: Security and compliance tracking

### Key Relationships
- Users can submit multiple fraud reports
- Entities can have multiple fraud reports
- Reports are linked to countries through entities
- All actions are logged in audit logs

## 🚀 Deployment

### Quick Deploy to Vercel (Recommended)

Deploy your RMGFraud application to Vercel in minutes:

#### Prerequisites
- GitHub account
- Vercel account (free at [vercel.com](https://vercel.com))
- External PostgreSQL database (see database setup below)

#### Step 1: Prepare Your Repository
```bash
# Ensure all files are committed
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

#### Step 2: Set Up External Database
Since Vercel doesn't support persistent databases, you need an external PostgreSQL database:

**Option A: Supabase (Free tier available)**
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Get your database URL from Settings > Database
4. Format: `postgresql://postgres:[password]@[host]:5432/postgres`

**Option B: Railway PostgreSQL**
1. Go to [railway.app](https://railway.app)
2. Create new project > Database > PostgreSQL
3. Get connection string from Variables tab

**Option C: Neon (Free tier)**
1. Go to [neon.tech](https://neon.tech)
2. Create free account and database
3. Get connection string

#### Step 3: Deploy to Vercel

**Method 1: Vercel CLI (Recommended)**
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from your project directory
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (Choose your account)
# - Link to existing project? N
# - Project name: rmgfraud
# - Directory: ./
# - Override settings? N
```

**Method 2: Vercel Dashboard**
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your Git repository
4. Vercel will auto-detect it's a Python project

#### Step 4: Configure Environment Variables
In your Vercel project dashboard, go to Settings > Environment Variables and add:

```env
# Required
SECRET_KEY=your-very-secure-secret-key-here
DATABASE_URL=postgresql://username:password@host:port/database_name
FLASK_ENV=production

# Optional but recommended
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

#### Step 5: Initialize Database
After deployment, initialize your database:

```bash
# Set environment variables locally
export DATABASE_URL=your_postgresql_url
export SECRET_KEY=your_secret_key

# Initialize database
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database initialized successfully!')
"

# Create admin user
python create_admin.py
```

#### Step 6: Test Your Deployment
1. Visit your Vercel URL (e.g., `https://rmgfraud.vercel.app`)
2. Test the main functionality
3. Verify database operations work
4. Check authentication flow

#### Quick Deploy Script
```bash
# Use the provided deployment script
./deploy-vercel.sh

# Or test configuration locally first
python3 test-vercel.py
```

### Alternative Deployment Options

#### Railway (Easiest for Flask apps)
```bash
# Use the provided deployment script
./deploy-railway.sh

# Or manually:
# 1. Go to railway.app
# 2. Connect GitHub repo
# 3. Add PostgreSQL database
# 4. Set environment variables
# 5. Deploy!
```

#### Render (Free tier available)
1. Connect GitHub repository
2. Add PostgreSQL database
3. Configure build command: `pip install -r requirements.txt`
4. Start command: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

#### Traditional VPS Deployment
```bash
# On Ubuntu server
sudo apt update
sudo apt install python3-pip postgresql nginx

# Install dependencies
pip3 install -r requirements.txt
pip3 install gunicorn psycopg2-binary

# Set up PostgreSQL
sudo -u postgres createdb rmgfraud
sudo -u postgres createuser rmgfraud_user

# Configure environment variables
export FLASK_ENV=production
export DATABASE_URL=postgresql://rmgfraud_user:password@localhost/rmgfraud
export SECRET_KEY=your-secret-key

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

#### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

### Deployment Considerations

#### Vercel Limitations
- ⚠️ **Database Timeouts**: 10-second limit (hobby plan)
- ⚠️ **No Persistent Storage**: SQLite won't work
- ⚠️ **File Upload Limits**: 4.5MB max
- ⚠️ **Cold Starts**: Functions may be slow on first request

#### Recommended for Production
- **Railway**: Best for Flask apps with databases
- **Render**: Good free tier, better than Vercel for Flask
- **Heroku**: Traditional, well-supported
- **AWS/GCP/Azure**: Enterprise with auto-scaling

### Environment Variables Reference

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Flask secret key | Yes | `your-secret-key-here` |
| `DATABASE_URL` | Database connection | Yes | `postgresql://user:pass@host/db` |
| `FLASK_ENV` | Environment | Yes | `production` |
| `MAIL_SERVER` | SMTP server | No | `smtp.gmail.com` |
| `MAIL_USERNAME` | Email username | No | `your-email@gmail.com` |
| `MAIL_PASSWORD` | Email password | No | `your-app-password` |
| `ADMIN_EMAIL` | Admin email | No | `admin@yourdomain.com` |
| `ADMIN_PASSWORD` | Admin password | No | `your-admin-password` |

### Troubleshooting

#### Common Issues
1. **App won't start**: Check environment variables
2. **Database connection fails**: Verify `DATABASE_URL` format
3. **Static files not loading**: Ensure files are in `static/` directory
4. **Email not working**: Check SMTP credentials

#### Debug Commands
```bash
# Test locally
python run.py

# Check database connection
python -c "
from app import app, db
with app.app_context():
    print('Database connected:', db.engine.url)
"

# Verify environment variables
python -c "
import os
print('SECRET_KEY:', bool(os.environ.get('SECRET_KEY')))
print('DATABASE_URL:', bool(os.environ.get('DATABASE_URL')))
"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Roadmap

- [ ] Advanced analytics dashboard
- [ ] Machine learning fraud detection
- [ ] Mobile application
- [ ] API for third-party integrations
- [ ] Advanced reporting features
- [ ] Multi-language support

## 🙏 Acknowledgments

- Bootstrap for the responsive framework
- Chart.js for data visualization
- Leaflet for interactive maps
- Flask community for the excellent framework
- All contributors and users of the platform

---

**RMGFraud** - Protecting the Ready-Made Garment industry through technology and community collaboration.
