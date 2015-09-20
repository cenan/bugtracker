BEGIN TRANSACTION;

CREATE TABLE user_filter (
	id integer primary key,
	user_id integer,
	filter VARCHAR(255)
);

COMMIT;



