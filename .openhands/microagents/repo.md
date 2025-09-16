# RMGfraud Repository Guide

## Project Description

RMGfraud is a comprehensive fraud detection platform specifically designed for the Ready-Made Garment (RMG) industry. It provides a secure, minimalist, and user-contributed system for identifying and addressing fraud within the garment manufacturing sector. The platform features anonymous reporting capabilities, comprehensive entity databases, country-level analytics, and interactive visualizations to help combat fraud in the RMG supply chain.

## Technology Stack

- **Backend**: Python Flask with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: Flask-Login with Multi-Factor Authentication (MFA)
- **Security**: CSRF protection, secure headers, end-to-end encryption
- **Visualization**: Chart.js, Leaflet.js for interactive maps

## File Structure Overview

```
RMGfraud/
├── app.py                 # Main Flask application entry point
├── run.py                 # Development server runner
├── config.py             # Configuration settings
├── models.py             # SQLAlchemy database models
├── create_admin.py       # Admin user creation script
├── requirements.txt      # Python dependencies
├── routes/               # Route blueprints
│   ├── auth.py          # Authentication routes
│   ├── dashboard.py     # Dashboard routes
│   ├── database.py      # Database management routes
│   ├── reporting.py     # Fraud reporting routes
│   └── country.py       # Country profile routes
├── templates/           # Jinja2 HTML templates
│   ├── base.html        # Base template
│   ├── auth/            # Authentication templates
│   ├── dashboard/       # Dashboard templates
│   ├── database/        # Database templates
│   ├── reporting/       # Reporting templates
│   └── country/         # Country profile templates
├── static/              # Static assets
│   ├── css/style.css    # Custom stylesheets
│   └── js/main.js       # JavaScript functionality
└── instance/            # Instance-specific files (SQLite DB)
```

## Getting Started

### Prerequisites
- Python 3.11+
- pip (Python package installer)
- PostgreSQL (for production) or SQLite (for development)

### Quick Setup
1. **Install dependencies**: `pip install -r requirements.txt`
2. **Set up environment**: Copy `config.py` to `.env` and configure your settings
3. **Initialize database**: The app will create tables automatically on first run
4. **Create admin user**: `python create_admin.py`
5. **Run the application**: `python run.py` or `python app.py`

The application will be available at `http://localhost:5000`

## Testing and Development

### Running Tests
- **Setup test**: `python test_setup.py` - Validates imports, configuration, database connection, and routes
- **Vercel test**: `python test-vercel.py` - Tests Vercel deployment configuration

### Development Commands
- **Development server**: `python run.py` (includes debug mode and auto-reload)
- **Production server**: `python app.py` or use gunicorn: `gunicorn -w 4 -b 0.0.0.0:8000 app:app`
- **Database operations**: Flask-Migrate is configured for database migrations

## Deployment Options

The project includes deployment configurations for multiple platforms:
- **Vercel**: Use `deploy-vercel.sh` or follow the detailed Vercel deployment guide in README.md
- **Railway**: Use `deploy-railway.sh` for easy Railway deployment
- **Traditional VPS**: Standard Flask deployment with gunicorn and nginx
- **Docker**: Dockerfile included for containerized deployment

## Key Features for Developers

- **Security-first design**: MFA, CSRF protection, secure headers, input sanitization
- **Modular architecture**: Blueprint-based routing for maintainable code
- **Responsive UI**: Bootstrap 5 with custom dark theme
- **Database flexibility**: Supports both SQLite (dev) and PostgreSQL (prod)
- **Comprehensive logging**: Audit trails and security logging built-in
- **API-ready**: JSON endpoints available for data visualization and external integrations

## Environment Variables

Essential configuration variables (see `config.py` for full list):
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string
- `FLASK_ENV`: Environment (development/production)
- `MAIL_*`: Email configuration for notifications