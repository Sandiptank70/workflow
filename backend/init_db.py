#!/usr/bin/env python3
"""
Simple database initialization script for Docker
"""

def main():
    print("=" * 60)
    print("Initializing Database...")
    print("=" * 60)
    
    try:
        # Import after we're in the right directory
        from app.database import init_db, engine
        from app.services import IntegrationService
        from app.database import SessionLocal
        
        # Test connection
        print("\n1. Testing database connection...")
        try:
            with engine.connect() as conn:
                conn.execute("SELECT 1")
                print("✅ Database connection successful!")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
        
        # Create tables
        print("\n2. Creating database tables...")
        try:
            init_db()
            print("✅ Database tables created!")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False
        
        # Check tables
        print("\n3. Verifying tables exist...")
        try:
            with engine.connect() as conn:
                result = conn.execute("SHOW TABLES")
                tables = [row[0] for row in result]
                print(f"✅ Found tables: {tables}")
        except Exception as e:
            print(f"❌ Error checking tables: {e}")
            return False
        
        # Check integration types
        print("\n4. Checking integration types...")
        db = SessionLocal()
        try:
            types = IntegrationService.get_integration_types(db)
            print(f"✅ Found {len(types)} integration types")
            for t in types:
                print(f"   - {t.name}")
        except Exception as e:
            print(f"❌ Error checking integration types: {e}")
        finally:
            db.close()
        
        print("\n" + "=" * 60)
        print("✅ Initialization Complete!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)