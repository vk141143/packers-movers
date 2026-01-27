-- Rename scheduled_date and scheduled_time to preferred_date and preferred_time
ALTER TABLE jobs RENAME COLUMN scheduled_date TO preferred_date;
ALTER TABLE jobs RENAME COLUMN scheduled_time TO preferred_time;
