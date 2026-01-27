-- Migration: Add cancellation_reason column to jobs table
-- This separates job cancellation reasons from quote decline reasons

ALTER TABLE jobs ADD COLUMN cancellation_reason VARCHAR(255);

-- Comment explaining the difference:
-- decline_reason: Used when client declines a quote (free text)
-- cancellation_reason: Used when client cancels a booking (predefined options like "Financial constraints", "Schedule conflict", etc.)
