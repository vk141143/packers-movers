-- Run this SQL directly on your production database if table creation still fails
-- Connect to: public-primary-pg-inmumbaizone2-189645-1657841.db.onutho.com:5432
-- Database: packers (or defaultdb)

CREATE TABLE IF NOT EXISTS clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    full_name VARCHAR,
    company_name VARCHAR,
    phone_number VARCHAR,
    client_type VARCHAR,
    address VARCHAR,
    profile_photo VARCHAR,
    is_verified BOOLEAN DEFAULT FALSE,
    otp VARCHAR,
    otp_expiry TIMESTAMP,
    otp_method VARCHAR,
    reset_otp VARCHAR,
    reset_otp_expiry TIMESTAMP,
    reset_token VARCHAR,
    reset_token_expiry TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_clients_id ON clients(id);
CREATE INDEX IF NOT EXISTS ix_clients_email ON clients(email);

-- Verify table was created
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'clients' 
ORDER BY ordinal_position;
