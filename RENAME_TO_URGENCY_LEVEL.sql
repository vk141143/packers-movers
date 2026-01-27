-- Rename service_levels table to urgency_levels
-- Run this on client_backend database (packers database)

-- Step 1: Rename the table
ALTER TABLE service_levels RENAME TO urgency_levels;

-- Step 2: Update jobs table column name
ALTER TABLE jobs RENAME COLUMN service_level TO urgency_level;

-- Step 3: Add comments
COMMENT ON TABLE urgency_levels IS 'Urgency levels for job response times (Standard, Urgent, Emergency)';
COMMENT ON COLUMN jobs.urgency_level IS 'References urgency_levels table';

-- Verify the changes
SELECT * FROM urgency_levels;
