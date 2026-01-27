-- Remove price_gbp column from urgency_levels table
ALTER TABLE urgency_levels DROP COLUMN IF EXISTS price_gbp;
