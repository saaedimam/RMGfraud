from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import FraudReport, Entity, db, AuditLog
from datetime import datetime
import bleach
import json

bp = Blueprint('reporting', __name__, url_prefix='/reporting')

@bp.route('/submit', methods=['GET', 'POST'])
def submit():
    """Anonymous fraud reporting form"""
    if request.method == 'POST':
        title = bleach.clean(request.form.get('title', ''))
        fraud_type = request.form.get('fraud_type', '')
        risk_level = request.form.get('risk_level', '')
        summary = bleach.clean(request.form.get('summary', ''))
        detailed_description = bleach.clean(request.form.get('detailed_description', ''))
        entity_name = bleach.clean(request.form.get('entity_name', ''))
        entity_type = request.form.get('entity_type', '')
        country_code = request.form.get('country_code', '')
        sources = request.form.get('sources', '')
        is_anonymous = request.form.get('is_anonymous') == 'on'
        
        # Validation
        if not title or not fraud_type or not risk_level or not summary:
            flash('Title, fraud type, risk level, and summary are required.', 'error')
            return render_template('reporting/submit.html')
        
        # Process sources
        sources_list = []
        if sources:
            sources_list = [s.strip() for s in sources.split('\n') if s.strip()]
        
        # Create or find entity
        entity = None
        if entity_name and entity_type and country_code:
            entity = Entity.query.filter_by(
                name=entity_name,
                entity_type=entity_type,
                country_code=country_code
            ).first()
            
            if not entity:
                entity = Entity(
                    name=entity_name,
                    entity_type=entity_type,
                    country_code=country_code,
                    risk_level=risk_level,
                    is_verified=False
                )
                db.session.add(entity)
                db.session.flush()  # Get the ID
        
        # Create fraud report
        fraud_report = FraudReport(
            title=title,
            fraud_type=fraud_type,
            risk_level=risk_level,
            summary=summary,
            detailed_description=detailed_description,
            sources=json.dumps(sources_list),
            is_anonymous=is_anonymous,
            entity_id=entity.id if entity else None,
            reporter_id=current_user.id if current_user.is_authenticated and not is_anonymous else None,
            status='pending',
            priority='high' if risk_level in ['High', 'Critical'] else 'medium'
        )
        
        db.session.add(fraud_report)
        db.session.commit()
        
        # Create audit log
        audit_log = AuditLog(
            user_id=current_user.id if current_user.is_authenticated else None,
            action='submit_fraud_report',
            resource_type='fraud_report',
            resource_id=fraud_report.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details=f'Anonymous: {is_anonymous}, Risk level: {risk_level}',
            timestamp=datetime.utcnow()
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash('Fraud report submitted successfully! It will be reviewed by our team.', 'success')
        return redirect(url_for('reporting.success'))
    
    return render_template('reporting/submit.html')

@bp.route('/success')
def success():
    """Success page after report submission"""
    return render_template('reporting/success.html')

@bp.route('/my-reports')
@login_required
def my_reports():
    """User's submitted reports"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    reports = FraudReport.query.filter_by(reporter_id=current_user.id).order_by(
        FraudReport.created_at.desc()
    ).paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template('reporting/my_reports.html', reports=reports)

@bp.route('/report/<int:id>')
@login_required
def report_detail(id):
    """Detailed view of a fraud report"""
    report = FraudReport.query.get_or_404(id)
    
    # Check permissions
    if report.reporter_id != current_user.id and current_user.role not in ['admin', 'moderator']:
        flash('You do not have permission to view this report.', 'error')
        return redirect(url_for('reporting.my_reports'))
    
    # Parse sources
    sources = []
    if report.sources:
        try:
            sources = json.loads(report.sources)
        except json.JSONDecodeError:
            sources = [report.sources]
    
    return render_template('reporting/report_detail.html', 
                         report=report, 
                         sources=sources)

@bp.route('/moderate')
@login_required
def moderate():
    """Moderation panel for admin/moderator users"""
    if current_user.role not in ['admin', 'moderator']:
        flash('You do not have permission to access the moderation panel.', 'error')
        return redirect(url_for('dashboard.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    status = request.args.get('status', 'pending')
    
    query = FraudReport.query
    if status != 'all':
        query = query.filter_by(status=status)
    
    reports = query.order_by(FraudReport.created_at.desc()).paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template('reporting/moderate.html', 
                         reports=reports, 
                         status=status)

@bp.route('/review/<int:id>', methods=['POST'])
@login_required
def review_report(id):
    """Review and approve/reject fraud report"""
    if current_user.role not in ['admin', 'moderator']:
        flash('You do not have permission to review reports.', 'error')
        return redirect(url_for('reporting.moderate'))
    
    report = FraudReport.query.get_or_404(id)
    review_status = request.form.get('review_status', '')
    review_notes = bleach.clean(request.form.get('review_notes', ''))
    
    if review_status not in ['approved', 'rejected', 'needs_more_info']:
        flash('Invalid review status.', 'error')
        return redirect(url_for('reporting.moderate'))
    
    # Update report status
    if review_status == 'approved':
        report.status = 'verified'
    elif review_status == 'rejected':
        report.status = 'rejected'
    else:
        report.status = 'under_review'
    
    report.updated_at = datetime.utcnow()
    
    # Create review record
    from models import ReportReview
    review = ReportReview(
        fraud_report_id=report.id,
        reviewer_id=current_user.id,
        review_status=review_status,
        review_notes=review_notes
    )
    
    db.session.add(review)
    db.session.commit()
    
    # Create audit log
    audit_log = AuditLog(
        user_id=current_user.id,
        action='review_fraud_report',
        resource_type='fraud_report',
        resource_id=report.id,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        details=f'Status: {review_status}, Notes: {review_notes}',
        timestamp=datetime.utcnow()
    )
    db.session.add(audit_log)
    db.session.commit()
    
    flash(f'Report {review_status} successfully!', 'success')
    return redirect(url_for('reporting.moderate'))

@bp.route('/api/fraud-types')
def fraud_types():
    """API endpoint for fraud types"""
    fraud_types = [
        'Financial Fraud',
        'Supply Chain Fraud',
        'Labor Violations',
        'Environmental Violations',
        'Document Forgery',
        'Bribery and Corruption',
        'Tax Evasion',
        'Money Laundering',
        'Intellectual Property Theft',
        'Quality Control Fraud',
        'Safety Violations',
        'Other'
    ]
    
    return jsonify(fraud_types)
