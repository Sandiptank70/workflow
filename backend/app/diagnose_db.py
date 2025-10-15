#!/usr/bin/env python3
"""
Database Initialization and Troubleshooting Script
Run this to diagnose and fix database issues
"""

import sys
import os

# Add the app directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Change to the script's directory
os.chdir(current_dir)

def check_database_connection():
    """Check if database connection works"""
    print("=" * 60)
    print("1. Checking Database Connection...")
    print("=" * 60)
    
    try:
        from app.database import engine
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\nPossible fixes:")
        print("1. Check if MariaDB/MySQL is running: systemctl status mariadb")
        print("2. Verify database exists: mysql -u root -p -e 'SHOW DATABASES;'")
        print("3. Check credentials in backend/.env file")
        return False

def check_database_exists():
    """Check if the database exists"""
    print("\n" + "=" * 60)
    print("2. Checking if Database Exists...")
    print("=" * 60)
    
    try:
        from app.database import engine, DB_NAME
        with engine.connect() as conn:
            result = conn.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{DB_NAME}'")
            if result.fetchone():
                print(f"✅ Database '{DB_NAME}' exists!")
                return True
            else:
                print(f"❌ Database '{DB_NAME}' does not exist!")
                print(f"\nTo create it, run:")
                print(f"mysql -u root -p -e \"CREATE DATABASE {DB_NAME};\"")
                return False
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

def create_tables():
    """Create database tables"""
    print("\n" + "=" * 60)
    print("3. Creating Database Tables...")
    print("=" * 60)
    
    try:
        from app.database import init_db
        init_db()
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def check_tables():
    """Check if tables exist"""
    print("\n" + "=" * 60)
    print("4. Checking Database Tables...")
    print("=" * 60)
    
    try:
        from app.database import engine
        with engine.connect() as conn:
            result = conn.execute("SHOW TABLES")
            tables = [row[0] for row in result]
            
            expected_tables = ['integration_types', 'integrations', 'workflows', 'execution_logs']
            
            print(f"Found tables: {tables}")
            
            all_exist = all(table in tables for table in expected_tables)
            
            if all_exist:
                print("✅ All required tables exist!")
                return True
            else:
                missing = [t for t in expected_tables if t not in tables]
                print(f"❌ Missing tables: {missing}")
                return False
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def check_encryption():
    """Check if encryption is working"""
    print("\n" + "=" * 60)
    print("5. Checking Encryption...")
    print("=" * 60)
    
    try:
        from app.utils.encryption import encryption_service
        test_data = "test_secret_123"
        encrypted = encryption_service.encrypt(test_data)
        decrypted = encryption_service.decrypt(encrypted)
        
        if decrypted == test_data:
            print("✅ Encryption working correctly!")
            return True
        else:
            print("❌ Encryption/decryption mismatch!")
            return False
    except Exception as e:
        print(f"❌ Encryption error: {e}")
        return False

def test_api_endpoint():
    """Test if the integration types endpoint works"""
    print("\n" + "=" * 60)
    print("6. Testing API Endpoint...")
    print("=" * 60)
    
    try:
        from sqlalchemy.orm import Session
        from app.database import SessionLocal
        from app.services import IntegrationService
        
        db = SessionLocal()
        try:
            types = IntegrationService.get_integration_types(db)
            print(f"✅ API endpoint working! Found {len(types)} integration types")
            
            if len(types) > 0:
                print("\nExisting integration types:")
                for t in types:
                    print(f"  - {t.name}")
            else:
                print("\nNo integration types found yet.")
                print("Run: python setup_integration_types.py")
            
            return True
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ API endpoint error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main diagnostic function"""
    print("\n" + "=" * 60)
    print("WORKFLOW AUTOMATION PLATFORM - DATABASE DIAGNOSTICS")
    print("=" * 60)
    
    # Check connection
    if not check_database_connection():
        print("\n❌ Cannot proceed without database connection!")
        sys.exit(1)
    
    # Check if database exists (optional check)
    check_database_exists()
    
    # Create/update tables
    create_tables()
    
    # Check tables
    if not check_tables():
        print("\n❌ Tables are missing or incorrect!")
        print("Try running this script again or manually create the database.")
        sys.exit(1)
    
    # Check encryption
    if not check_encryption():
        print("\n❌ Encryption is not working!")
        print("Check your ENCRYPTION_KEY in .env file")
        sys.exit(1)
    
    # Test API
    test_api_endpoint()
    
    print("\n" + "=" * 60)
    print("✅ ALL CHECKS PASSED!")
    print("=" * 60)
    print("\nYour database is ready to use!")
    print("\nNext steps:")
    print("1. Start the backend: uvicorn app.main:app --reload")
    print("2. Initialize sample data: python setup_integration_types.py")
    print("3. Start the frontend: cd ../frontend && npm run dev")
    print("4. Open: http://localhost:3000")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()