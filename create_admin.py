#!/usr/bin/env python3
"""
Admin user creation script for RMGFraud platform
Run this script to create the initial admin user
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User

def create_admin_user():
    """Create the initial admin user"""
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(role='admin').first()
        if admin:
            print("Admin user already exists!")
            print(f"Username: {admin.username}")
            print(f"Email: {admin.email}")
            return
        
        # Get admin details
        print("Creating admin user for RMGFraud platform...")
        print("=" * 50)
        
        username = input("Enter admin username: ").strip()
        email = input("Enter admin email: ").strip()
        password = input("Enter admin password: ").strip()
        verification_id = input("Enter verification ID (BGMEA/RMG/Banking): ").strip()
        verification_type = input("Enter verification type (bgmea/rmg_supplier/banking): ").strip()
        
        if not all([username, email, password, verification_id, verification_type]):
            print("Error: All fields are required!")
            return
        
        # Create admin user
        admin = User(
            username=username,
            email=email,
            verification_id=verification_id,
            verification_type=verification_type,
            role='admin',
            is_verified=True,
            created_at=datetime.utcnow()
        )
        admin.set_password(password)
        
        try:
            db.session.add(admin)
            db.session.commit()
            
            print("\n" + "=" * 50)
            print("✅ Admin user created successfully!")
            print(f"Username: {admin.username}")
            print(f"Email: {admin.email}")
            print(f"Role: {admin.role}")
            print(f"Verification ID: {admin.verification_id}")
            print(f"Verification Type: {admin.verification_type}")
            print("=" * 50)
            print("\nYou can now log in to the admin panel.")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {e}")

def create_sample_data():
    """Create sample data for testing"""
    with app.app_context():
        print("\nCreating sample data...")
        
        # Create sample entities
        from models import Entity, CountryProfile
        
        # Sample countries
        countries = [
            {'country_name': 'Bangladesh', 'country_code': 'BD', 'fraud_count': 15, 'high_risk_count': 5, 'critical_count': 2},
            {'country_name': 'India', 'country_code': 'IN', 'fraud_count': 12, 'high_risk_count': 3, 'critical_count': 1},
            {'country_name': 'Pakistan', 'country_code': 'PK', 'fraud_count': 8, 'high_risk_count': 2, 'critical_count': 1},
            {'country_name': 'China', 'country_code': 'CN', 'fraud_count': 20, 'high_risk_count': 8, 'critical_count': 3},
        ]
        
        for country_data in countries:
            country = CountryProfile.query.filter_by(country_code=country_data['country_code']).first()
            if not country:
                country = CountryProfile(**country_data)
                db.session.add(country)
        
        # Sample entities
        entities = [
            {'name': 'ABC Garments Ltd', 'entity_type': 'company', 'country_code': 'BD', 'risk_level': 'High', 'is_verified': True},
            {'name': 'XYZ Textiles', 'entity_type': 'company', 'country_code': 'IN', 'risk_level': 'Medium', 'is_verified': True},
            {'name': 'Global Suppliers Inc', 'entity_type': 'supplier', 'country_code': 'CN', 'risk_level': 'Critical', 'is_verified': False},
            {'name': 'John Smith', 'entity_type': 'individual', 'country_code': 'BD', 'risk_level': 'Low', 'is_verified': True},
        ]
        
        for entity_data in entities:
            entity = Entity.query.filter_by(name=entity_data['name']).first()
            if not entity:
                entity = Entity(**entity_data)
                db.session.add(entity)
        
        try:
            db.session.commit()
            print("✅ Sample data created successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating sample data: {e}")

if __name__ == '__main__':
    print("RMGFraud - Admin Setup Script")
    print("=" * 40)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database tables created/verified")
    
    # Create admin user
    create_admin_user()
    
    # Ask if user wants to create sample data
    create_sample = input("\nCreate sample data for testing? (y/n): ").strip().lower()
    if create_sample == 'y':
        create_sample_data()
    
    print("\n🎉 Setup complete! You can now run the application with: python app.py")
