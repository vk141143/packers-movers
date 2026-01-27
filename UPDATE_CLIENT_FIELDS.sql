-- Add new columns to clients table and rename address to business_address
ALTER TABLE clients ADD COLUMN IF NOT EXISTS contact_person_name VARCHAR;
ALTER TABLE clients ADD COLUMN IF NOT EXISTS department VARCHAR;
ALTER TABLE clients RENAME COLUMN address TO business_address;
