"""Test script to verify database and email connectivity"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE, override=True)

print("=" * 60)
print("TESTING DATABASE AND EMAIL CONFIGURATION")
print("=" * 60)

# Test 1: Check environment variables
print("\n1. CHECKING ENVIRONMENT VARIABLES:")
print("-" * 60)
DATABASE_URL = os.getenv("DATABASE_URL")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

if DATABASE_URL:
    # Mask password in URL
    print(f"✅ DATABASE_URL: Found")
    print(f"   Protocol: {DATABASE_URL.split('://')[0]}")
    print(f"   Database: {DATABASE_URL.split('/')[-1]}")
else:
    print("❌ DATABASE_URL: NOT FOUND")

if SMTP_USER:
    print(f"✅ SMTP_USER: {SMTP_USER}")
else:
    print("❌ SMTP_USER: NOT FOUND")

if SMTP_PASSWORD:
    print(f"✅ SMTP_PASSWORD: {'*' * len(SMTP_PASSWORD)} (length: {len(SMTP_PASSWORD)})")
else:
    print("❌ SMTP_PASSWORD: NOT FOUND")

# Test 2: Database Connection
print("\n2. TESTING DATABASE CONNECTION:")
print("-" * 60)
try:
    from sqlalchemy import create_engine, text
    
    # Convert to psycopg2 if needed
    sync_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg2://")
    
    engine = create_engine(sync_url, pool_pre_ping=True)
    
    with engine.connect() as conn:
        # Test connection
        result = conn.execute(text("SELECT version()"))
        version = result.scalar()
        print(f"✅ Database connected successfully!")
        print(f"   PostgreSQL version: {version[:50]}...")
        
        # Check database name
        result = conn.execute(text("SELECT current_database()"))
        db_name = result.scalar()
        print(f"   Database name: {db_name}")
        
        # Check if clients table exists
        result = conn.execute(text(
            "SELECT EXISTS (SELECT FROM information_schema.tables "
            "WHERE table_schema = 'public' AND table_name = 'clients')"
        ))
        table_exists = result.scalar()
        
        if table_exists:
            print(f"✅ 'clients' table exists")
            
            # Count clients
            result = conn.execute(text("SELECT COUNT(*) FROM clients"))
            count = result.scalar()
            print(f"   Total clients in database: {count}")
        else:
            print(f"⚠️  'clients' table does NOT exist")
            
except Exception as e:
    print(f"❌ Database connection FAILED: {e}")

# Test 3: Email Connection
print("\n3. TESTING EMAIL (SMTP) CONNECTION:")
print("-" * 60)
try:
    import smtplib
    
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    
    print(f"   Connecting to {smtp_server}:{smtp_port}...")
    
    server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
    server.starttls()
    
    print(f"✅ SMTP server connected")
    print(f"   Authenticating as {SMTP_USER}...")
    
    server.login(SMTP_USER, SMTP_PASSWORD)
    print(f"✅ SMTP authentication successful!")
    
    server.quit()
    print(f"✅ Email system is working correctly")
    
except Exception as e:
    print(f"❌ Email connection FAILED: {e}")
    print(f"   This may cause registration to work but emails won't be sent")

# Test 4: Test OTP Email Send (Optional)
print("\n4. TESTING OTP EMAIL SEND (DRY RUN):")
print("-" * 60)
try:
    from app.core.email import send_otp_email
    
    test_email = SMTP_USER  # Send to yourself
    test_otp = "1234"
    
    print(f"   Sending test OTP to {test_email}...")
    send_otp_email(test_email, test_otp)
    print(f"✅ Test email sent successfully!")
    print(f"   Check your inbox: {test_email}")
    
except Exception as e:
    print(f"❌ Test email FAILED: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)
