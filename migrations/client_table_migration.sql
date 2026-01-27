-- Migration for Client table columns
-- Run this on your live database if columns are missing

-- Add missing columns to clients table
ALTER TABLE clients ADD COLUMN IF NOT EXISTS contact_person_name VARCHAR;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS department VARCHAR;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS client_type VARCHAR;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS business_address VARCHAR;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS profile_photo VARCHAR;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS otp_method VARCHAR;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS reset_otp VARCHAR;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS reset_otp_expiry TIMESTAMP;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS reset_token VARCHAR;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS reset_token_expiry TIMESTAMP;

-- Add cancellation_reason to jobs table
ALTER TABLE jobs ADD COLUMN IF NOT EXISTS cancellation_reason VARCHAR;

-- Verify columns were added
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'clients' 
ORDER BY ordinal_position;
