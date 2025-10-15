#!/usr/bin/env python3
"""
Super Simple: Just add the column with raw SQL
No inspection, no checks - just do it
"""

import sys
import os
import sqlite3

print("=" * 60)
print("Quick Migration: Add 'tasks' Column")
print("=" * 60)

# Database file path
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'workflow_automation.db')

print(f"\nDatabase: {db_path}")

if not os.path.exists(db_path):
    print(f"\n❌ Database file not found at: {db_path}")
    print("\nPlease run this first:")
    print("  python3 -c 'from app.database import init_db; init_db()'")
    sys.exit(1)

try:
    print("\n📝 Connecting to database...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("📝 Adding 'tasks' column...")
    
    try:
        cursor.execute("ALTER TABLE integration_types ADD COLUMN tasks TEXT")
        conn.commit()
        print("✅ Column 'tasks' added successfully!")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("✅ Column 'tasks' already exists!")
        else:
            raise
    
    # Verify
    print("\n📝 Verifying...")
    cursor.execute("PRAGMA table_info(integration_types)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'tasks' in columns:
        print("✅ Verification successful!")
        print(f"\nColumns in integration_types: {', '.join(columns)}")
    else:
        print("❌ Verification failed!")
        sys.exit(1)
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ Migration Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Restart backend:")
    print("   cd ..")
    print("   docker-compose restart backend")
    print("")
    print("2. Test API:")
    print("   curl http://localhost:8000/api/import-export/export/all")
    print("")
    
    sys.exit(0)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)