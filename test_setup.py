#!/usr/bin/env python3
"""
RMGFraud Setup Test Script
Test the basic functionality of the application
"""

import os
import sys
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from app import app, db
        print("✅ Flask app and database imported successfully")
    except Exception as e:
        print(f"❌ Error importing Flask app: {e}")
        return False
    
    try:
        from models import User, Entity, FraudReport, CountryProfile
        print("✅ Database models imported successfully")
    except Exception as e:
        print(f"❌ Error importing models: {e}")
        return False
    
    try:
        from routes import auth, dashboard, database, reporting, country
        print("✅ Route blueprints imported successfully")
    except Exception as e:
        print(f"❌ Error importing routes: {e}")
        return False
    
    return True

def test_database_connection():
    """Test database connection and table creation"""
    print("\nTesting database connection...")
    
    try:
        from app import app, db
        
        with app.app_context():
            # Test database connection
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Test basic query
            from models import User
            user_count = User.query.count()
            print(f"✅ Database query successful (Users: {user_count})")
            
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        traceback.print_exc()
        return False

def test_routes():
    """Test if routes are properly registered"""
    print("\nTesting route registration...")
    
    try:
        from app import app
        
        with app.app_context():
            # Check if routes are registered
            routes = [str(rule) for rule in app.url_map.iter_rules()]
            
            expected_routes = [
                '/',
                '/auth/login',
                '/auth/register',
                '/database/',
                '/reporting/submit',
                '/country/',
                '/dashboard/'
            ]
            
            missing_routes = []
            for route in expected_routes:
                if not any(route in r for r in routes):
                    missing_routes.append(route)
            
            if missing_routes:
                print(f"❌ Missing routes: {missing_routes}")
                return False
            else:
                print("✅ All expected routes registered")
                return True
                
    except Exception as e:
        print(f"❌ Route testing error: {e}")
        return False

def test_configuration():
    """Test application configuration"""
    print("\nTesting configuration...")
    
    try:
        from app import app
        
        # Check essential configuration
        if not app.config.get('SECRET_KEY'):
            print("❌ SECRET_KEY not configured")
            return False
        
        if not app.config.get('SQLALCHEMY_DATABASE_URI'):
            print("❌ Database URI not configured")
            return False
        
        print("✅ Basic configuration looks good")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Run all tests"""
    print("RMGFraud Setup Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_configuration,
        test_database_connection,
        test_routes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\nNext steps:")
        print("1. Run: python create_admin.py")
        print("2. Run: python run.py")
        print("3. Open: http://localhost:5000")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
