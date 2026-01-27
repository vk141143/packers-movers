-- Update urgency levels to match UI specifications
-- Standard: 48-72 hours (72h max) - Base price +£0
-- Urgent: 24-48 hours (48h) - Additional +£150
-- Emergency: Same day (24h) - Additional +£300

-- Delete old urgency levels
DELETE FROM urgency_levels;

-- Insert new urgency levels with correct pricing modifiers
INSERT INTO urgency_levels (id, name, sla_hours, price_gbp, is_active, created_at, updated_at)
VALUES 
    (gen_random_uuid()::text, 'Standard', 72, 0, true, NOW(), NOW()),
    (gen_random_uuid()::text, 'Urgent', 48, 150, true, NOW(), NOW()),
    (gen_random_uuid()::text, 'Emergency', 24, 300, true, NOW(), NOW());
