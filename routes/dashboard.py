from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import User, Entity, FraudReport, CountryProfile, db, AuditLog
from datetime import datetime, timedelta
import bleach

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def index():
    """User dashboard with overview statistics"""
    # Get user statistics
    user_reports = FraudReport.query.filter_by(reporter_id=current_user.id).count()
    recent_reports = FraudReport.query.filter_by(reporter_id=current_user.id).order_by(
        FraudReport.created_at.desc()
    ).limit(5).all()
    
    # Get platform statistics
    total_entities = Entity.query.count()
    high_risk_entities = Entity.query.filter(Entity.risk_level.in_(['High', 'Critical'])).count()
    total_reports = FraudReport.query.count()
    verified_reports = FraudReport.query.filter_by(status='verified').count()
    
    # Get recent activity
    recent_activity = AuditLog.query.filter_by(user_id=current_user.id).order_by(
        AuditLog.timestamp.desc()
    ).limit(10).all()
    
    return render_template('dashboard/index.html',
                         user_reports=user_reports,
                         recent_reports=recent_reports,
                         total_entities=total_entities,
                         high_risk_entities=high_risk_entities,
                         total_reports=total_reports,
                         verified_reports=verified_reports,
                         recent_activity=recent_activity)

@bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('dashboard/profile.html', user=current_user)

@bp.route('/settings')
@login_required
def settings():
    """User settings page"""
    return render_template('dashboard/settings.html', user=current_user)

@bp.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    username = bleach.clean(request.form.get('username', ''))
    email = bleach.clean(request.form.get('email', ''))
    
    # Check if username/email already exists
    if username != current_user.username:
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('dashboard.profile'))
        current_user.username = username
    
    if email != current_user.email:
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('dashboard.profile'))
        current_user.email = email
    
    db.session.commit()
    
    # Create audit log
    audit_log = AuditLog(
        user_id=current_user.id,
        action='update_profile',
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        timestamp=datetime.utcnow()
    )
    db.session.add(audit_log)
    db.session.commit()
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('dashboard.profile'))

@bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    # Validation
    if not current_user.check_password(current_password):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('dashboard.settings'))
    
    if new_password != confirm_password:
        flash('New passwords do not match.', 'error')
        return redirect(url_for('dashboard.settings'))
    
    if len(new_password) < 8:
        flash('Password must be at least 8 characters long.', 'error')
        return redirect(url_for('dashboard.settings'))
    
    # Update password
    current_user.set_password(new_password)
    db.session.commit()
    
    # Create audit log
    audit_log = AuditLog(
        user_id=current_user.id,
        action='change_password',
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        timestamp=datetime.utcnow()
    )
    db.session.add(audit_log)
    db.session.commit()
    
    flash('Password changed successfully!', 'success')
    return redirect(url_for('dashboard.settings'))

@bp.route('/admin')
@login_required
def admin():
    """Admin panel for platform management"""
    if current_user.role != 'admin':
        flash('You do not have permission to access the admin panel.', 'error')
        return redirect(url_for('dashboard.index'))
    
    # Get platform statistics
    total_users = User.query.count()
    verified_users = User.query.filter_by(is_verified=True).count()
    pending_verifications = User.query.filter_by(is_verified=False).count()
    
    total_entities = Entity.query.count()
    verified_entities = Entity.query.filter_by(is_verified=True).count()
    pending_entities = Entity.query.filter_by(is_verified=False).count()
    
    total_reports = FraudReport.query.count()
    pending_reports = FraudReport.query.filter_by(status='pending').count()
    verified_reports = FraudReport.query.filter_by(status='verified').count()
    
    # Get recent activity
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_reports = FraudReport.query.order_by(FraudReport.created_at.desc()).limit(5).all()
    
    return render_template('dashboard/admin.html',
                         total_users=total_users,
                         verified_users=verified_users,
                         pending_verifications=pending_verifications,
                         total_entities=total_entities,
                         verified_entities=verified_entities,
                         pending_entities=pending_entities,
                         total_reports=total_reports,
                         pending_reports=pending_reports,
                         verified_reports=verified_reports,
                         recent_users=recent_users,
                         recent_reports=recent_reports)

@bp.route('/verify-user/<int:user_id>', methods=['POST'])
@login_required
def verify_user(user_id):
    """Verify user account (admin only)"""
    if current_user.role != 'admin':
        flash('You do not have permission to verify users.', 'error')
        return redirect(url_for('dashboard.admin'))
    
    user = User.query.get_or_404(user_id)
    user.is_verified = True
    db.session.commit()
    
    # Create audit log
    audit_log = AuditLog(
        user_id=current_user.id,
        action='verify_user',
        resource_type='user',
        resource_id=user.id,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        details=f'Verified user: {user.username}',
        timestamp=datetime.utcnow()
    )
    db.session.add(audit_log)
    db.session.commit()
    
    flash(f'User {user.username} has been verified!', 'success')
    return redirect(url_for('dashboard.admin'))

@bp.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete user account (admin only)"""
    if current_user.role != 'admin':
        flash('You do not have permission to delete users.', 'error')
        return redirect(url_for('dashboard.admin'))
    
    user = User.query.get_or_404(user_id)
    
    # Prevent self-deletion
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('dashboard.admin'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    # Create audit log
    audit_log = AuditLog(
        user_id=current_user.id,
        action='delete_user',
        resource_type='user',
        resource_id=user_id,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        details=f'Deleted user: {username}',
        timestamp=datetime.utcnow()
    )
    db.session.add(audit_log)
    db.session.commit()
    
    flash(f'User {username} has been deleted!', 'success')
    return redirect(url_for('dashboard.admin'))

@bp.route('/audit-logs')
@login_required
def audit_logs():
    """View audit logs (admin only)"""
    if current_user.role != 'admin':
        flash('You do not have permission to view audit logs.', 'error')
        return redirect(url_for('dashboard.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template('dashboard/audit_logs.html', logs=logs)
