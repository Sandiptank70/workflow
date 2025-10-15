"""
Migration script to add tasks column to integration_types table
Run this after updating the model
"""
import sys
import os

# Add parent directory to Python path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text, inspect

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./workflow_automation.db")

engine = create_engine(DATABASE_URL)

def check_table_exists(table_name):
    """Check if a table exists"""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()

def check_column_exists(table_name, column_name):
    """Check if a column exists in a table"""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def create_tables():
    """Create all tables if they don't exist"""
    print("Creating tables if they don't exist...")
    try:
        from app.database import init_db
        init_db()
        print("✅ Tables created/verified!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        print(f"\nPlease run these commands first:")
        print(f"  cd {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}")
        print(f"  python3 -c 'from app.database import init_db; init_db()'")
        return False

def upgrade():
    """Add tasks column to integration_types table"""
    # First, check if tables exist
    if not check_table_exists('integration_types'):
        print("⚠️  Table 'integration_types' does not exist.")
        print("   Creating tables first...")
        if not create_tables():
            return False
    
    # Now check if column already exists
    if check_column_exists('integration_types', 'tasks'):
        print("✅ Column 'tasks' already exists in integration_types table")
        return True
    
    # Add the column
    with engine.connect() as conn:
        try:
            conn.execute(text("""
                ALTER TABLE integration_types 
                ADD COLUMN tasks TEXT
            """))
            conn.commit()
            print("✅ Successfully added 'tasks' column to integration_types table")
            return True
        except Exception as e:
            print(f"❌ Error adding column: {e}")
            return False

def downgrade():
    """Remove tasks column from integration_types table"""
    with engine.connect() as conn:
        try:
            # Note: SQLite doesn't support DROP COLUMN directly
            # For production with PostgreSQL/MySQL, use:
            # conn.execute(text("ALTER TABLE integration_types DROP COLUMN tasks"))
            print("⚠️  Downgrade not fully supported for SQLite")
            print("   For SQLite, you would need to recreate the table")
        except Exception as e:
            print(f"Error during downgrade: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Running Database Migration")
    print("=" * 60)
    
    success = upgrade()
    
    print("=" * 60)
    if success:
        print("✅ Migration Complete!")
        sys.exit(0)
    else:
        print("❌ Migration Failed!")
        sys.exit(1)