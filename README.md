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

### Production Deployment

1. **Set up production environment**
   ```bash
   export FLASK_ENV=production
   export DATABASE_URL=postgresql://user:pass@localhost/rmgfraud
   ```

2. **Install production dependencies**
   ```bash
   pip install gunicorn psycopg2-binary
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

### Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
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
