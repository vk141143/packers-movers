import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Convert asyncpg URL to psycopg2 format
if DATABASE_URL and "asyncpg" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

print(f"Connecting to database...")

try:
    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    print("Creating clients table...")
    
    # Create clients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            full_name VARCHAR(255),
            company_name VARCHAR(255),
            phone_number VARCHAR(50),
            client_type VARCHAR(100),
            address TEXT,
            profile_photo VARCHAR(500),
            is_verified BOOLEAN DEFAULT FALSE,
            otp VARCHAR(10),
            otp_expiry TIMESTAMP,
            otp_method VARCHAR(20),
            reset_otp VARCHAR(10),
            reset_otp_expiry TIMESTAMP,
            reset_token VARCHAR(255),
            reset_token_expiry TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    print("Creating indexes...")
    
    # Create indexes
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email);
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_clients_phone ON clients(phone_number);
    """)
    
    # Commit changes
    conn.commit()
    
    print("✅ Clients table created successfully!")
    
    # Verify table exists
    cursor.execute("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_name = 'clients';
    """)
    
    result = cursor.fetchone()
    if result:
        print(f"✅ Verified: Table '{result[0]}' exists in database")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
