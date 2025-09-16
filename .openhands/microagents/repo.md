# RMGFraud - Fraud Detection Platform

## Project Description

RMGFraud is a secure, minimalist fraud detection platform specifically designed for the Ready-Made Garment (RMG) industry. The platform provides a comprehensive database for tracking fraudulent entities, anonymous reporting capabilities, country-level analytics, and interactive visualizations. Built with Flask and featuring multi-factor authentication, role-based access control, and end-to-end encryption, it serves as a community-driven solution to combat fraud in the garment manufacturing sector.

## File Structure Overview

```
RMGfraud/
├── app.py                 # Main Flask application with configuration and blueprint registration
├── models.py             # SQLAlchemy database models (User, Entity, FraudReport, CountryProfile)
├── config.py             # Application configuration settings
├── requirements.txt      # Python dependencies
├── routes/               # Route blueprints organized by functionality
│   ├── auth.py          # Authentication and user management routes
│   ├── dashboard.py     # Main dashboard and analytics routes
│   ├── database.py      # Entity database search and management
│   ├── reporting.py     # Fraud reporting submission routes
│   └── country.py       # Country profile and statistics routes
├── templates/           # Jinja2 HTML templates
│   ├── base.html        # Base template with common layout
│   ├── index.html       # Homepage template
│   ├── auth/            # Authentication-related templates
│   ├── dashboard/       # Dashboard templates
│   ├── database/        # Database search templates
│   ├── reporting/       # Fraud reporting templates
│   └── country/         # Country profile templates
├── static/              # Static assets (CSS, JavaScript, images)
│   ├── css/style.css    # Main stylesheet with dark theme
│   └── js/main.js       # Client-side JavaScript functionality
├── create_admin.py      # Script to create initial admin user
├── run.py              # Development server runner
└── test_setup.py       # Setup validation and testing script
```

## Running Tests and Commands

### Setup and Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Test the setup
python test_setup.py

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Create admin user
python create_admin.py

# Run development server
python app.py
# or
python run.py
```

### Testing
- **Setup Test**: `python test_setup.py` - Validates imports, database connection, routes, and configuration
- **Vercel Test**: `python test-vercel.py` - Tests deployment configuration for Vercel
- **Manual Testing**: The application includes comprehensive error handling and logging for manual testing

### Database Management
```bash
# Database migrations
flask db migrate -m "Description of changes"
flask db upgrade

# Reset database (development only)
flask db downgrade
flask db upgrade
```

## Developer Information

### Technology Stack
- **Backend**: Python Flask with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: Flask-Login with TOTP-based MFA
- **Security**: CSRF protection, secure headers, input sanitization

### Key Features
- Multi-factor authentication with QR code setup
- Role-based access control (Admin, Moderator, User)
- Anonymous fraud reporting with encryption
- Interactive country-level analytics and heatmaps
- Advanced search and filtering capabilities
- Comprehensive audit logging

### Environment Variables
Create a `.env` file with:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///rmgfraud.db  # or PostgreSQL URL for production
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Deployment Options
The project includes deployment configurations for:
- **Vercel**: `deploy-vercel.sh` and `vercel.json`
- **Railway**: `deploy-railway.sh` and `railway.json`
- **Traditional VPS**: Gunicorn + Nginx setup instructions in README

### Security Considerations
- All forms include CSRF protection
- User input is sanitized using bleach
- Passwords are hashed with bcrypt
- MFA is enforced for admin accounts
- Audit logging tracks all significant actions