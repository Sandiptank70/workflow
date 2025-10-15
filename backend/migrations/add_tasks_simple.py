#!/usr/bin/env python3
"""
Bulletproof migration: Add tasks column
This version handles all edge cases properly
"""

import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 60)
print("Database Migration: Add 'tasks' Column")
print("=" * 60)

try:
    print("\n1️⃣ Importing dependencies...")
    from app.database import Base, engine
    from sqlalchemy import inspect, text
    
    print("✅ Dependencies loaded")
    
    print("\n2️⃣ Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created/verified")
    
    print("\n3️⃣ Checking if 'tasks' column exists...")
    
    # Create a new connection to check
    with engine.connect() as conn:
        # Try to query the column
        try:
            result = conn.execute(text("SELECT tasks FROM integration_types LIMIT 1"))
            result.close()
            print("✅ Column 'tasks' already exists!")
            print("\n" + "=" * 60)
            print("✅ Nothing to do - Migration already complete!")
            print("=" * 60)
            sys.exit(0)
        except Exception:
            # Column doesn't exist, need to add it
            pass
    
    print("📝 Column 'tasks' not found, adding it now...")
    
    print("\n4️⃣ Adding 'tasks' column...")
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE integration_types ADD COLUMN tasks TEXT"))
        conn.commit()
    
    print("✅ Column 'tasks' added successfully!")
    
    print("\n5️⃣ Verifying column was added...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT tasks FROM integration_types LIMIT 1"))
        result.close()
    print("✅ Verification successful!")
    
    print("\n" + "=" * 60)
    print("✅ Migration Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Restart backend: docker-compose restart backend")
    print("2. Test API: curl http://localhost:8000/api/import-export/export/all")
    print("3. Import sample: curl -X POST http://localhost:8000/api/import-export/import/integration-types -d @sample-teams-integration-type.json")
    print("")
    
    sys.exit(0)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nDebug info:")
    print(f"Working directory: {os.getcwd()}")
    print(f"Python path: {sys.path[0]}")
    import traceback
    traceback.print_exc()
    sys.exit(1)