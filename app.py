from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import pyotp
import qrcode
from io import BytesIO
import base64
import bleach
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///rmgfraud.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = True

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
csrf = CSRFProtect(app)

# Import and initialize models
from models import init_db, User, Entity, FraudReport, CountryProfile
init_db(db)

# Import routes
from routes import auth, dashboard, database, reporting, country

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(database.bp)
app.register_blueprint(reporting.bp)
app.register_blueprint(country.bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    """Homepage with search bar, fraud heatmap, and red-flag cases"""
    # Get recent high-risk fraud reports for the carousel
    recent_frauds = FraudReport.query.filter(
        FraudReport.risk_level.in_(['High', 'Critical'])
    ).order_by(FraudReport.created_at.desc()).limit(5).all()
    
    # Get fraud statistics for heatmap
    fraud_stats = db.session.query(
        CountryProfile.country_code,
        CountryProfile.fraud_count
    ).all()
    
    return render_template('index.html', 
                         recent_frauds=recent_frauds,
                         fraud_stats=fraud_stats)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
