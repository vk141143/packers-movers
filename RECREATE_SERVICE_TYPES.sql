-- Drop old service_types table with UUID
DROP TABLE IF EXISTS service_types CASCADE;

-- Create service_types table with integer ID
CREATE TABLE service_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Insert service types
INSERT INTO service_types (name, description, is_active, created_at, updated_at)
VALUES 
    ('Emergency Clearance', 'Urgent same-day service', true, NOW(), NOW()),
    ('House Clearance', 'Full property clearance', true, NOW(), NOW()),
    ('Office Clearance', 'Commercial spaces', true, NOW(), NOW()),
    ('Garden Clearance', 'Outdoor waste removal', true, NOW(), NOW());
