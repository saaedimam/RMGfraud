#!/usr/bin/env python3
"""
Simple RMGFraud Application - Working Version
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from datetime import datetime
import os

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rmgfraud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        # Use a simple hash for compatibility
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

# Entity model
class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    entity_type = db.Column(db.String(50), nullable=False)
    country_code = db.Column(db.String(3), nullable=False)
    risk_level = db.Column(db.String(20), default='Low')
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Fraud Report model
class FraudReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    fraud_type = db.Column(db.String(100), nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    is_anonymous = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    """Homepage"""
    recent_frauds = FraudReport.query.filter(
        FraudReport.risk_level.in_(['High', 'Critical'])
    ).order_by(FraudReport.created_at.desc()).limit(5).all()
    
    return render_template('index.html', recent_frauds=recent_frauds)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('auth/register.html')
        
        user = User(
            username=username,
            email=email,
            is_verified=True  # Auto-verify for demo
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/database')
def database():
    """Database page"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    search_query = request.args.get('q', '')
    entity_type = request.args.get('entity_type', '')
    risk_level = request.args.get('risk_level', '')
    
    query = Entity.query
    
    if search_query:
        query = query.filter(Entity.name.ilike(f'%{search_query}%'))
    
    if entity_type:
        query = query.filter(Entity.entity_type == entity_type)
    
    if risk_level:
        query = query.filter(Entity.risk_level == risk_level)
    
    entities = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template('database/index.html', entities=entities)

@app.route('/reporting/submit', methods=['GET', 'POST'])
def submit_report():
    """Fraud reporting form"""
    if request.method == 'POST':
        title = request.form.get('title', '')
        fraud_type = request.form.get('fraud_type', '')
        risk_level = request.form.get('risk_level', '')
        summary = request.form.get('summary', '')
        
        if not all([title, fraud_type, risk_level, summary]):
            flash('All fields are required.', 'error')
            return render_template('reporting/submit.html')
        
        fraud_report = FraudReport(
            title=title,
            fraud_type=fraud_type,
            risk_level=risk_level,
            summary=summary,
            is_anonymous=True,
            reporter_id=current_user.id if current_user.is_authenticated else None
        )
        
        db.session.add(fraud_report)
        db.session.commit()
        
        flash('Fraud report submitted successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('reporting/submit.html')

@app.route('/country')
def country():
    """Country profiles page"""
    countries = [
        {'country_name': 'Bangladesh', 'country_code': 'BD', 'fraud_count': 15},
        {'country_name': 'India', 'country_code': 'IN', 'fraud_count': 12},
        {'country_name': 'Pakistan', 'country_code': 'PK', 'fraud_count': 8},
        {'country_name': 'China', 'country_code': 'CN', 'fraud_count': 20},
    ]
    
    return render_template('country/index.html', countries=countries)

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user_reports = FraudReport.query.filter_by(reporter_id=current_user.id).count()
    total_entities = Entity.query.count()
    total_reports = FraudReport.query.count()
    
    return render_template('dashboard/index.html',
                         user_reports=user_reports,
                         total_entities=total_entities,
                         total_reports=total_reports)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@rmgfraud.com',
                role='admin',
                is_verified=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: username=admin, password=admin123")
    
    print("Starting RMGFraud application...")
    print("Admin login: username=admin, password=admin123")
    print("Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
