BEGIN TRANSACTION;

CREATE TABLE project (
	id integer primary key,
	project_name varchar(255)
);

ALTER TABLE issue ADD COLUMN project_id integer default 0;
ALTER TABLE category ADD COLUMN project_id integer default 0;
ALTER TABLE milestone ADD COLUMN project_id integer default 0;

COMMIT;

