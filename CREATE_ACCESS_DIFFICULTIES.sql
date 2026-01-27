-- Create access_difficulties table
CREATE TABLE IF NOT EXISTS access_difficulties (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Insert access difficulties
INSERT INTO access_difficulties (name, description, is_active, created_at, updated_at)
VALUES 
    ('Ground floor', 'Easy access', true, NOW(), NOW()),
    ('Stairs (no lift)', 'Manual carrying', true, NOW(), NOW()),
    ('Restricted parking', 'Limited vehicle access', true, NOW(), NOW()),
    ('Long carry distance', 'Extended walking', true, NOW(), NOW())
ON CONFLICT (name) DO NOTHING;
