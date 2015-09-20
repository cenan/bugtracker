BEGIN TRANSACTION;

ALTER TABLE milestone ADD COLUMN milestone_status integer default 0;
UPDATE milestone SET milestone_status = 0;

COMMIT;

