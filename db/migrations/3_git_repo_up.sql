BEGIN TRANSACTION;

ALTER TABLE project ADD COLUMN git_repo_path varchar(255);

COMMIT;

