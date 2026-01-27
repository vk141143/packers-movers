-- Remove furniture_items column from jobs table
ALTER TABLE jobs DROP COLUMN IF EXISTS furniture_items;
