#!/usr/bin/env python3
"""
Complete setup script for new features
Handles table creation, migration, and sample data import
"""

import os
import sys
import json
import requests
import time

def print_header(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def print_step(number, text):
    print(f"\n{number}. {text}")

def wait_for_backend(max_attempts=30):
    """Wait for backend to be ready"""
    print("   Waiting for backend to be ready...")
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print("   ✅ Backend is ready!")
                return True
        except:
            pass
        time.sleep(1)
        if (i + 1) % 5 == 0:
            print(f"   Still waiting... ({i + 1}s)")
    return False

def run_migration():
    """Run database migration"""
    print_step(1, "Running database migration...")
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    # Import and run migration
    try:
        from sqlalchemy import create_engine, inspect
        from app.database import init_db
        
        # Create tables first
        print("   Creating/verifying tables...")
        init_db()
        print("   ✅ Tables created/verified!")
        
        # Check if migration is needed
        DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./workflow_automation.db")
        engine = create_engine(DATABASE_URL)
        inspector = inspect(engine)
        
        columns = [col['name'] for col in inspector.get_columns('integration_types')]
        
        if 'tasks' in columns:
            print("   ✅ Column 'tasks' already exists!")
            return True
        
        # Run migration
        print("   Adding 'tasks' column...")
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE integration_types ADD COLUMN tasks TEXT"))
            conn.commit()
        
        print("   ✅ Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Migration error: {e}")
        return False

def restart_backend():
    """Restart backend service"""
    print_step(2, "Restarting backend service...")
    
    os.chdir(os.path.dirname(__file__))
    
    result = os.system("docker-compose restart backend")
    
    if result == 0:
        print("   ✅ Backend restart initiated!")
        return wait_for_backend()
    else:
        print("   ⚠️  Could not restart via docker-compose")
        print("   Please restart backend manually:")
        print("   docker-compose restart backend")
        return False

def test_api():
    """Test import/export API"""
    print_step(3, "Testing import/export API...")
    
    try:
        response = requests.get("http://localhost:8000/api/import-export/export/all", timeout=5)
        
        if response.status_code == 200:
            print("   ✅ Import/Export API is working!")
            data = response.json()
            print(f"   Found {len(data.get('integration_types', []))} integration types")
            print(f"   Found {len(data.get('workflows', []))} workflows")
            return True
        else:
            print(f"   ⚠️  API returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ API test failed: {e}")
        return False

def import_sample_data():
    """Import sample Teams integration type"""
    print_step(4, "Importing sample Teams integration type...")
    
    sample_file = os.path.join(os.path.dirname(__file__), 'sample-teams-integration-type.json')
    
    if not os.path.exists(sample_file):
        print("   ⚠️  Sample file not found, skipping...")
        return True
    
    try:
        with open(sample_file, 'r') as f:
            data = json.load(f)
        
        response = requests.post(
            "http://localhost:8000/api/import-export/import/integration-types",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Imported: {result.get('imported', 0)} types")
            print(f"   ⚠️  Skipped: {result.get('skipped', 0)} types (already exist)")
            if result.get('errors'):
                print(f"   ⚠️  Errors: {result['errors']}")
            return True
        else:
            print(f"   ❌ Import failed with status {response.status_code}")
            print(f"   {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

def verify_installation():
    """Verify everything is working"""
    print_step(5, "Verifying installation...")
    
    try:
        # Check integration types have tasks
        response = requests.get("http://localhost:8000/api/integration-types", timeout=5)
        
        if response.status_code != 200:
            print("   ❌ Could not fetch integration types")
            return False
        
        types = response.json()
        
        if not types:
            print("   ⚠️  No integration types found")
            print("   You may need to create integration types manually")
            return True
        
        # Check if any type has tasks
        types_with_tasks = [t for t in types if t.get('tasks')]
        
        if types_with_tasks:
            print(f"   ✅ Found {len(types_with_tasks)} integration type(s) with tasks defined!")
            for t in types_with_tasks[:3]:  # Show first 3
                task_count = len(t.get('tasks', []))
                print(f"      • {t['name']}: {task_count} tasks")
        else:
            print("   ⚠️  No integration types have tasks defined yet")
            print("   You can import the sample or add tasks manually")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Verification error: {e}")
        return False

def print_next_steps():
    """Print next steps for user"""
    print_header("✅ Setup Complete!")
    
    print("\n📚 What's available:")
    print("   1. Dynamic task selection with human-readable names")
    print("   2. Import/Export functionality for all components")
    print("")
    print("🔗 Try these commands:")
    print("   # Export everything")
    print("   curl http://localhost:8000/api/import-export/export/all | jq '.'")
    print("")
    print("   # Export only types")
    print("   curl http://localhost:8000/api/import-export/export/integration-types > types.json")
    print("")
    print("   # View integration types with tasks")
    print("   curl http://localhost:8000/api/integration-types | jq '.[0].tasks'")
    print("")
    print("📖 Documentation:")
    print("   • ALL_IN_ONE_GUIDE.md - Complete guide")
    print("   • QUICK_REF_NEW_FEATURES.md - Quick commands")
    print("   • IMPORT_EXPORT_TASKS_GUIDE.md - Detailed documentation")
    print("")
    print("🎉 Features are ready to use!")

def main():
    """Main setup function"""
    print_header("🚀 Setting Up New Features")
    print("   • Dynamic Task Selection")
    print("   • Import/Export Functionality")
    
    success = True
    
    # Step 1: Run migration
    if not run_migration():
        print("\n❌ Migration failed!")
        print("   Please check the error and try again")
        success = False
    
    # Step 2: Restart backend
    if success and not restart_backend():
        print("\n⚠️  Backend restart had issues")
        print("   Please restart manually: docker-compose restart backend")
        print("   Then run: python setup-complete.py --skip-restart")
        return False
    
    # Step 3: Test API
    if success and not test_api():
        print("\n⚠️  API test failed")
        print("   Backend may need more time to start")
        print("   Wait a moment and test manually:")
        print("   curl http://localhost:8000/api/import-export/export/all")
    
    # Step 4: Import sample
    if success:
        import_sample_data()
    
    # Step 5: Verify
    if success:
        verify_installation()
    
    # Print next steps
    if success:
        print_next_steps()
        return True
    else:
        print("\n❌ Setup had some issues")
        print("   Please check the errors above and consult the documentation")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)