#!/usr/bin/env python3
"""
Test script to verify Vercel configuration works locally
"""
import os
import sys
from pathlib import Path

# Add the root directory to Python path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Change working directory to root
os.chdir(root_dir)

def test_imports():
    """Test if all imports work correctly"""
    try:
        print("Testing imports...")
        from app import app, db
        print("✅ App and database imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_app_creation():
    """Test if Flask app can be created"""
    try:
        print("Testing Flask app creation...")
        from app import app
        print(f"✅ Flask app created: {app.name}")
        return True
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        print("Testing database connection...")
        from app import app, db
        
        with app.app_context():
            # Test database connection
            db.engine.execute("SELECT 1")
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Note: This is expected if DATABASE_URL is not set")
        return False

def test_vercel_handler():
    """Test Vercel handler function"""
    try:
        print("Testing Vercel handler...")
        from api.index import handler
        print("✅ Vercel handler imported successfully")
        return True
    except Exception as e:
        print(f"❌ Vercel handler failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Vercel Configuration")
    print("===============================")
    
    tests = [
        test_imports,
        test_app_creation,
        test_database_connection,
        test_vercel_handler
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your app is ready for Vercel deployment.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
