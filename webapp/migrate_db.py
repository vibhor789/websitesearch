"""
Database migration script to add new fields
Run this after deploying to add criteria and contact fields
"""
import sqlite3
import sys

def migrate_database(db_path='websearch.db'):
    """Add new fields to existing database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("🔄 Starting database migration...")

        # Add criteria fields to Search table
        try:
            cursor.execute("ALTER TABLE search ADD COLUMN missing_chatbox BOOLEAN DEFAULT 1")
            print("✓ Added missing_chatbox to search table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("⚠ missing_chatbox already exists")
            else:
                raise

        try:
            cursor.execute("ALTER TABLE search ADD COLUMN missing_whatsapp BOOLEAN DEFAULT 1")
            print("✓ Added missing_whatsapp to search table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("⚠ missing_whatsapp already exists")
            else:
                raise

        try:
            cursor.execute("ALTER TABLE search ADD COLUMN missing_call_button BOOLEAN DEFAULT 1")
            print("✓ Added missing_call_button to search table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("⚠ missing_call_button already exists")
            else:
                raise

        # Add contact fields to Lead table
        contact_fields = [
            ("emails", "TEXT"),
            ("phones", "TEXT"),
            ("contact_name", "VARCHAR(200)"),
            ("linkedin", "VARCHAR(500)"),
            ("facebook", "VARCHAR(500)"),
            ("twitter", "VARCHAR(500)"),
            ("instagram", "VARCHAR(500)")
        ]

        for field_name, field_type in contact_fields:
            try:
                cursor.execute(f"ALTER TABLE lead ADD COLUMN {field_name} {field_type}")
                print(f"✓ Added {field_name} to lead table")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e).lower():
                    print(f"⚠ {field_name} already exists")
                else:
                    raise

        conn.commit()
        print("\n✅ Database migration completed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'websearch.db'
    print(f"Migrating database: {db_path}\n")
    success = migrate_database(db_path)
    sys.exit(0 if success else 1)
