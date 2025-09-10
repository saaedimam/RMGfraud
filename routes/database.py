from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from models import Entity, FraudReport, db, AuditLog
from datetime import datetime
import bleach

bp = Blueprint('database', __name__, url_prefix='/database')

@bp.route('/')
def index():
    """Database main page with search and filters"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Get filter parameters
    search_query = bleach.clean(request.args.get('q', ''))
    entity_type = request.args.get('entity_type', '')
    risk_level = request.args.get('risk_level', '')
    country = request.args.get('country', '')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    # Build query
    query = Entity.query
    
    if search_query:
        query = query.filter(
            db.or_(
                Entity.name.ilike(f'%{search_query}%'),
                Entity.description.ilike(f'%{search_query}%'),
                Entity.registration_number.ilike(f'%{search_query}%')
            )
        )
    
    if entity_type:
        query = query.filter(Entity.entity_type == entity_type)
    
    if risk_level:
        query = query.filter(Entity.risk_level == risk_level)
    
    if country:
        query = query.filter(Entity.country_code == country)
    
    # Apply sorting
    if sort_by == 'name':
        query = query.order_by(Entity.name.asc() if sort_order == 'asc' else Entity.name.desc())
    elif sort_by == 'risk_level':
        risk_order = {'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}
        query = query.order_by(Entity.risk_level.asc() if sort_order == 'asc' else Entity.risk_level.desc())
    else:
        query = query.order_by(Entity.created_at.desc() if sort_order == 'desc' else Entity.created_at.asc())
    
    # Paginate results
    entities = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    # Get statistics
    total_entities = Entity.query.count()
    high_risk_count = Entity.query.filter(Entity.risk_level.in_(['High', 'Critical'])).count()
    verified_count = Entity.query.filter(Entity.is_verified == True).count()
    
    return render_template('database/index.html',
                         entities=entities,
                         search_query=search_query,
                         entity_type=entity_type,
                         risk_level=risk_level,
                         country=country,
                         sort_by=sort_by,
                         sort_order=sort_order,
                         total_entities=total_entities,
                         high_risk_count=high_risk_count,
                         verified_count=verified_count)

@bp.route('/search')
def search():
    """Search entities with AJAX support"""
    search_query = bleach.clean(request.args.get('q', ''))
    entity_type = request.args.get('entity_type', '')
    risk_level = request.args.get('risk_level', '')
    country = request.args.get('country', '')
    
    # Build query
    query = Entity.query
    
    if search_query:
        query = query.filter(
            db.or_(
                Entity.name.ilike(f'%{search_query}%'),
                Entity.description.ilike(f'%{search_query}%'),
                Entity.registration_number.ilike(f'%{search_query}%')
            )
        )
    
    if entity_type:
        query = query.filter(Entity.entity_type == entity_type)
    
    if risk_level:
        query = query.filter(Entity.risk_level == risk_level)
    
    if country:
        query = query.filter(Entity.country_code == country)
    
    entities = query.limit(50).all()
    
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify([{
            'id': entity.id,
            'name': entity.name,
            'entity_type': entity.entity_type,
            'risk_level': entity.risk_level,
            'country_code': entity.country_code,
            'is_verified': entity.is_verified
        } for entity in entities])
    
    return render_template('database/search_results.html', entities=entities)

@bp.route('/entity/<int:id>')
def entity_detail(id):
    """Detailed view of a specific entity"""
    entity = Entity.query.get_or_404(id)
    
    # Get related fraud reports
    fraud_reports = FraudReport.query.filter_by(entity_id=id).order_by(FraudReport.created_at.desc()).all()
    
    # Log view
    if current_user.is_authenticated:
        audit_log = AuditLog(
            user_id=current_user.id,
            action='view_entity',
            resource_type='entity',
            resource_id=entity.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            timestamp=datetime.utcnow()
        )
        db.session.add(audit_log)
        db.session.commit()
    
    return render_template('database/entity_detail.html', 
                         entity=entity, 
                         fraud_reports=fraud_reports)

@bp.route('/add-entity', methods=['GET', 'POST'])
@login_required
def add_entity():
    """Add new entity to database"""
    if not current_user.is_verified:
        flash('You must be verified to add entities.', 'error')
        return redirect(url_for('database.index'))
    
    if request.method == 'POST':
        name = bleach.clean(request.form.get('name', ''))
        entity_type = request.form.get('entity_type', '')
        country_code = request.form.get('country_code', '')
        registration_number = bleach.clean(request.form.get('registration_number', ''))
        contact_info = bleach.clean(request.form.get('contact_info', ''))
        description = bleach.clean(request.form.get('description', ''))
        risk_level = request.form.get('risk_level', 'Low')
        
        # Validation
        if not name or not entity_type or not country_code:
            flash('Name, entity type, and country are required.', 'error')
            return render_template('database/add_entity.html')
        
        # Create entity
        entity = Entity(
            name=name,
            entity_type=entity_type,
            country_code=country_code,
            registration_number=registration_number,
            contact_info=contact_info,
            description=description,
            risk_level=risk_level,
            is_verified=False  # Requires verification
        )
        
        db.session.add(entity)
        db.session.commit()
        
        # Create audit log
        audit_log = AuditLog(
            user_id=current_user.id,
            action='add_entity',
            resource_type='entity',
            resource_id=entity.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            details=f'Entity type: {entity_type}, Risk level: {risk_level}',
            timestamp=datetime.utcnow()
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash('Entity added successfully! It will be reviewed before being made public.', 'success')
        return redirect(url_for('database.entity_detail', id=entity.id))
    
    return render_template('database/add_entity.html')

@bp.route('/edit-entity/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entity(id):
    """Edit existing entity"""
    entity = Entity.query.get_or_404(id)
    
    # Check permissions
    if not current_user.is_verified and current_user.role not in ['admin', 'moderator']:
        flash('You do not have permission to edit entities.', 'error')
        return redirect(url_for('database.entity_detail', id=id))
    
    if request.method == 'POST':
        entity.name = bleach.clean(request.form.get('name', ''))
        entity.entity_type = request.form.get('entity_type', '')
        entity.country_code = request.form.get('country_code', '')
        entity.registration_number = bleach.clean(request.form.get('registration_number', ''))
        entity.contact_info = bleach.clean(request.form.get('contact_info', ''))
        entity.description = bleach.clean(request.form.get('description', ''))
        entity.risk_level = request.form.get('risk_level', 'Low')
        entity.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit log
        audit_log = AuditLog(
            user_id=current_user.id,
            action='edit_entity',
            resource_type='entity',
            resource_id=entity.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            timestamp=datetime.utcnow()
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash('Entity updated successfully!', 'success')
        return redirect(url_for('database.entity_detail', id=id))
    
    return render_template('database/edit_entity.html', entity=entity)

@bp.route('/verify-entity/<int:id>', methods=['POST'])
@login_required
def verify_entity(id):
    """Verify entity (admin/moderator only)"""
    if current_user.role not in ['admin', 'moderator']:
        flash('You do not have permission to verify entities.', 'error')
        return redirect(url_for('database.entity_detail', id=id))
    
    entity = Entity.query.get_or_404(id)
    entity.is_verified = True
    entity.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    # Create audit log
    audit_log = AuditLog(
        user_id=current_user.id,
        action='verify_entity',
        resource_type='entity',
        resource_id=entity.id,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        timestamp=datetime.utcnow()
    )
    db.session.add(audit_log)
    db.session.commit()
    
    flash('Entity verified successfully!', 'success')
    return redirect(url_for('database.entity_detail', id=id))
