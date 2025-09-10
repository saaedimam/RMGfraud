from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp

# This will be set by the app
db = None

def init_db(database):
    """Initialize the database instance"""
    global db
    db = database

class User(UserMixin, db.Model if db else object):
    """User model with authentication and role management"""
    if db:
        __tablename__ = 'users'
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password_hash = db.Column(db.String(128), nullable=False)
        role = db.Column(db.String(20), default='user')  # user, moderator, admin
        is_verified = db.Column(db.Boolean, default=False)
        verification_id = db.Column(db.String(50), unique=True)  # BGMEA, RMG Supplier, Banking ID
        verification_type = db.Column(db.String(20))  # bgmea, rmg_supplier, banking
        mfa_secret = db.Column(db.String(32))
        mfa_enabled = db.Column(db.Boolean, default=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        last_login = db.Column(db.DateTime)
        
        # Relationships
        fraud_reports = db.relationship('FraudReport', backref='reporter', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def generate_mfa_secret(self):
        """Generate MFA secret for user"""
        self.mfa_secret = pyotp.random_base32()
        return self.mfa_secret
    
    def verify_mfa_token(self, token):
        """Verify MFA token"""
        if not self.mfa_secret:
            return False
        totp = pyotp.TOTP(self.mfa_secret)
        return totp.verify(token, valid_window=1)
    
    def get_mfa_qr_code(self):
        """Generate QR code for MFA setup"""
        if not self.mfa_secret:
            return None
        totp = pyotp.TOTP(self.mfa_secret)
        qr_code = qrcode.make(totp.provisioning_uri(
            name=self.email,
            issuer_name="RMGFraud"
        ))
        return qr_code

class Entity(db.Model if db else object):
    """Entity model for companies, individuals, suppliers, etc."""
    if db:
        __tablename__ = 'entities'
        
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(200), nullable=False)
        entity_type = db.Column(db.String(50), nullable=False)  # company, individual, supplier, manufacturer
        country_code = db.Column(db.String(3), nullable=False)
        registration_number = db.Column(db.String(100))
        contact_info = db.Column(db.Text)
        description = db.Column(db.Text)
        risk_level = db.Column(db.String(20), default='Low')  # Low, Medium, High, Critical
        is_verified = db.Column(db.Boolean, default=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        # Relationships
        fraud_reports = db.relationship('FraudReport', backref='entity', lazy='dynamic')

class FraudReport(db.Model if db else object):
    """Fraud report model for whistleblower submissions"""
    if db:
        __tablename__ = 'fraud_reports'
        
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(200), nullable=False)
        fraud_type = db.Column(db.String(100), nullable=False)
        risk_level = db.Column(db.String(20), nullable=False)  # Low, Medium, High, Critical
        summary = db.Column(db.Text, nullable=False)
        detailed_description = db.Column(db.Text)
        sources = db.Column(db.Text)  # JSON string of source information
        evidence_files = db.Column(db.Text)  # JSON string of file paths
        is_anonymous = db.Column(db.Boolean, default=True)
        status = db.Column(db.String(20), default='pending')  # pending, under_review, verified, rejected
        priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        # Foreign keys
        entity_id = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=True)
        reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
        
        # Relationships
        reviews = db.relationship('ReportReview', backref='fraud_report', lazy='dynamic')

class ReportReview(db.Model if db else object):
    """Review model for fraud report moderation"""
    if db:
        __tablename__ = 'report_reviews'
        
        id = db.Column(db.Integer, primary_key=True)
        fraud_report_id = db.Column(db.Integer, db.ForeignKey('fraud_reports.id'), nullable=False)
        reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        review_status = db.Column(db.String(20), nullable=False)  # approved, rejected, needs_more_info
        review_notes = db.Column(db.Text)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        # Relationships
        reviewer = db.relationship('User', backref='reviews')

class CountryProfile(db.Model if db else object):
    """Country profile model for fraud statistics and heatmap data"""
    if db:
        __tablename__ = 'country_profiles'
        
        id = db.Column(db.Integer, primary_key=True)
        country_name = db.Column(db.String(100), nullable=False)
        country_code = db.Column(db.String(3), unique=True, nullable=False)
        fraud_count = db.Column(db.Integer, default=0)
        high_risk_count = db.Column(db.Integer, default=0)
        critical_count = db.Column(db.Integer, default=0)
        last_updated = db.Column(db.DateTime, default=datetime.utcnow)
        
        # Additional statistics
        total_entities = db.Column(db.Integer, default=0)
        verified_entities = db.Column(db.Integer, default=0)
        fraud_trend = db.Column(db.String(20))  # increasing, decreasing, stable

class AuditLog(db.Model if db else object):
    """Audit log for security and compliance tracking"""
    if db:
        __tablename__ = 'audit_logs'
        
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
        action = db.Column(db.String(100), nullable=False)
        resource_type = db.Column(db.String(50))
        resource_id = db.Column(db.Integer)
        ip_address = db.Column(db.String(45))
        user_agent = db.Column(db.Text)
        timestamp = db.Column(db.DateTime, default=datetime.utcnow)
        details = db.Column(db.Text)  # JSON string for additional details
        
        # Relationships
        user = db.relationship('User', backref='audit_logs')