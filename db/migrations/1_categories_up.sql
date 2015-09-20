BEGIN TRANSACTION;

CREATE TABLE category (
	id integer primary key,
	category_name varchar(255),
	default_assignee_id integer
);

INSERT INTO category (id, category_name) VALUES (0, 'None');


ALTER TABLE issue ADD COLUMN category_id integer default 0;

ALTER TABLE issue_update ADD COLUMN old_category integer default 0;
ALTER TABLE issue_update ADD COLUMN new_category integer default 0;


DROP VIEW issue_update_view;

CREATE VIEW issue_update_view AS
SELECT * FROM
  issue_update
JOIN
  user ON issue_update.user_id=user.id
JOIN
  milestone old_ms ON issue_update.old_milestone=old_ms.id
JOIN
  milestone new_ms ON issue_update.new_milestone=new_ms.id
JOIN
  category old_cat ON issue_update.old_category=old_cat.id
JOIN
  category new_cat ON issue_update.new_category=new_cat.id;

COMMIT;

