from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, AuditLog
from datetime import datetime
import pyotp
import qrcode
from io import BytesIO
import base64
import bleach

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login with MFA support"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = bleach.clean(request.form.get('username', ''))
        password = request.form.get('password', '')
        mfa_token = request.form.get('mfa_token', '')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # Check MFA if enabled
            if user.mfa_enabled:
                if not mfa_token:
                    session['pending_user_id'] = user.id
                    return render_template('auth/mfa_verify.html', user=user)
                
                if not user.verify_mfa_token(mfa_token):
                    flash('Invalid MFA token. Please try again.', 'error')
                    return render_template('auth/mfa_verify.html', user=user)
            
            # Log successful login
            login_user(user)
            user.last_login = datetime.utcnow()
            
            # Create audit log
            audit_log = AuditLog(
                user_id=user.id,
                action='login',
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                timestamp=datetime.utcnow()
            )
            db.session.add(audit_log)
            db.session.commit()
            
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with verification requirements"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = bleach.clean(request.form.get('username', ''))
        email = bleach.clean(request.form.get('email', ''))
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        verification_id = bleach.clean(request.form.get('verification_id', ''))
        verification_type = request.form.get('verification_type', '')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('auth/register.html')
        
        if not verification_id or not verification_type:
            flash('Verification ID and type are required.', 'error')
            return render_template('auth/register.html')
        
        # Create user
        user = User(
            username=username,
            email=email,
            verification_id=verification_id,
            verification_type=verification_type,
            is_verified=False  # Requires admin verification
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Create audit log
        audit_log = AuditLog(
            user_id=user.id,
            action='register',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details=f'Verification type: {verification_type}',
            timestamp=datetime.utcnow()
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash('Registration successful! Your account is pending verification by an administrator.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@bp.route('/logout')
@login_required
def logout():
    """User logout"""
    # Create audit log
    audit_log = AuditLog(
        user_id=current_user.id,
        action='logout',
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        timestamp=datetime.utcnow()
    )
    db.session.add(audit_log)
    db.session.commit()
    
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@bp.route('/setup-mfa')
@login_required
def setup_mfa():
    """Setup MFA for user"""
    if current_user.mfa_enabled:
        flash('MFA is already enabled for your account.', 'info')
        return redirect(url_for('dashboard.settings'))
    
    secret = current_user.generate_mfa_secret()
    db.session.commit()
    
    # Generate QR code
    qr_code = current_user.get_mfa_qr_code()
    qr_buffer = BytesIO()
    qr_code.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    qr_data = base64.b64encode(qr_buffer.getvalue()).decode()
    
    return render_template('auth/setup_mfa.html', 
                         secret=secret, 
                         qr_code=qr_data)

@bp.route('/verify-mfa', methods=['POST'])
@login_required
def verify_mfa():
    """Verify MFA setup"""
    token = request.form.get('token', '')
    
    if current_user.verify_mfa_token(token):
        current_user.mfa_enabled = True
        db.session.commit()
        
        flash('MFA has been successfully enabled!', 'success')
        return redirect(url_for('dashboard.settings'))
    else:
        flash('Invalid token. Please try again.', 'error')
        return redirect(url_for('auth.setup_mfa'))

@bp.route('/disable-mfa', methods=['POST'])
@login_required
def disable_mfa():
    """Disable MFA for user"""
    password = request.form.get('password', '')
    
    if not current_user.check_password(password):
        flash('Invalid password.', 'error')
        return redirect(url_for('dashboard.settings'))
    
    current_user.mfa_enabled = False
    current_user.mfa_secret = None
    db.session.commit()
    
    flash('MFA has been disabled.', 'success')
    return redirect(url_for('dashboard.settings'))
