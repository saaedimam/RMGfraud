from flask import Blueprint, render_template, request, jsonify
from models import CountryProfile, Entity, FraudReport, db
from datetime import datetime, timedelta
import json

bp = Blueprint('country', __name__, url_prefix='/country')

@bp.route('/')
def index():
    """Country profiles overview page"""
    countries = CountryProfile.query.order_by(CountryProfile.fraud_count.desc()).all()
    
    # Get global statistics
    total_fraud_count = sum(country.fraud_count for country in countries)
    total_high_risk = sum(country.high_risk_count for country in countries)
    total_critical = sum(country.critical_count for country in countries)
    
    return render_template('country/index.html',
                         countries=countries,
                         total_fraud_count=total_fraud_count,
                         total_high_risk=total_high_risk,
                         total_critical=total_critical)

@bp.route('/<country_code>')
def country_detail(country_code):
    """Detailed country profile with statistics and visualizations"""
    country = CountryProfile.query.filter_by(country_code=country_code).first()
    
    if not country:
        # Create country profile if it doesn't exist
        country = CountryProfile(
            country_name=country_code,
            country_code=country_code,
            fraud_count=0,
            high_risk_count=0,
            critical_count=0
        )
        db.session.add(country)
        db.session.commit()
    
    # Get entities in this country
    entities = Entity.query.filter_by(country_code=country_code).all()
    
    # Get fraud reports related to entities in this country
    fraud_reports = FraudReport.query.join(Entity).filter(
        Entity.country_code == country_code
    ).order_by(FraudReport.created_at.desc()).limit(20).all()
    
    # Calculate statistics
    entity_stats = {
        'total': len(entities),
        'verified': len([e for e in entities if e.is_verified]),
        'high_risk': len([e for e in entities if e.risk_level in ['High', 'Critical']]),
        'by_type': {}
    }
    
    # Group by entity type
    for entity in entities:
        entity_type = entity.entity_type
        if entity_type not in entity_stats['by_type']:
            entity_stats['by_type'][entity_type] = 0
        entity_stats['by_type'][entity_type] += 1
    
    # Get fraud trends (last 12 months)
    twelve_months_ago = datetime.utcnow() - timedelta(days=365)
    monthly_reports = db.session.query(
        db.func.date_trunc('month', FraudReport.created_at).label('month'),
        db.func.count(FraudReport.id).label('count')
    ).filter(
        FraudReport.created_at >= twelve_months_ago
    ).group_by(
        db.func.date_trunc('month', FraudReport.created_at)
    ).order_by('month').all()
    
    # Get fraud types distribution
    fraud_types = db.session.query(
        FraudReport.fraud_type,
        db.func.count(FraudReport.id).label('count')
    ).join(Entity).filter(
        Entity.country_code == country_code
    ).group_by(FraudReport.fraud_type).all()
    
    return render_template('country/country_detail.html',
                         country=country,
                         entities=entities,
                         fraud_reports=fraud_reports,
                         entity_stats=entity_stats,
                         monthly_reports=monthly_reports,
                         fraud_types=fraud_types)

@bp.route('/api/statistics')
def api_statistics():
    """API endpoint for country statistics"""
    countries = CountryProfile.query.all()
    
    statistics = []
    for country in countries:
        statistics.append({
            'country_code': country.country_code,
            'country_name': country.country_name,
            'fraud_count': country.fraud_count,
            'high_risk_count': country.high_risk_count,
            'critical_count': country.critical_count,
            'total_entities': country.total_entities,
            'verified_entities': country.verified_entities,
            'fraud_trend': country.fraud_trend
        })
    
    return jsonify(statistics)

@bp.route('/api/heatmap-data')
def api_heatmap_data():
    """API endpoint for fraud heatmap data"""
    countries = CountryProfile.query.all()
    
    heatmap_data = []
    for country in countries:
        # Calculate risk score based on fraud count and risk levels
        risk_score = country.fraud_count + (country.high_risk_count * 2) + (country.critical_count * 3)
        
        heatmap_data.append({
            'country_code': country.country_code,
            'country_name': country.country_name,
            'fraud_count': country.fraud_count,
            'risk_score': risk_score,
            'coordinates': get_country_coordinates(country.country_code)
        })
    
    return jsonify(heatmap_data)

@bp.route('/update-statistics')
def update_statistics():
    """Update country statistics (admin only)"""
    # This would typically be called by a scheduled task
    countries = CountryProfile.query.all()
    
    for country in countries:
        # Count entities in this country
        total_entities = Entity.query.filter_by(country_code=country.country_code).count()
        verified_entities = Entity.query.filter_by(
            country_code=country.country_code,
            is_verified=True
        ).count()
        
        # Count fraud reports
        fraud_reports = FraudReport.query.join(Entity).filter(
            Entity.country_code == country.country_code
        ).all()
        
        fraud_count = len(fraud_reports)
        high_risk_count = len([r for r in fraud_reports if r.risk_level == 'High'])
        critical_count = len([r for r in fraud_reports if r.risk_level == 'Critical'])
        
        # Update country profile
        country.fraud_count = fraud_count
        country.high_risk_count = high_risk_count
        country.critical_count = critical_count
        country.total_entities = total_entities
        country.verified_entities = verified_entities
        country.last_updated = datetime.utcnow()
        
        # Calculate trend (simplified)
        if fraud_count > 0:
            country.fraud_trend = 'increasing'  # This would be calculated based on historical data
        else:
            country.fraud_trend = 'stable'
    
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Statistics updated'})

def get_country_coordinates(country_code):
    """Get approximate coordinates for country (simplified)"""
    coordinates = {
        'BD': [23.6850, 90.3563],  # Bangladesh
        'IN': [20.5937, 78.9629],  # India
        'PK': [30.3753, 69.3451],  # Pakistan
        'CN': [35.8617, 104.1954], # China
        'LK': [7.8731, 80.7718],   # Sri Lanka
        'MM': [21.9162, 95.9560],  # Myanmar
        'TH': [15.8700, 100.9925], # Thailand
        'VN': [14.0583, 108.2772], # Vietnam
        'ID': [-0.7893, 113.9213], # Indonesia
        'MY': [4.2105, 101.9758],  # Malaysia
    }
    
    return coordinates.get(country_code, [0, 0])
