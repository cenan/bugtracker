BEGIN TRANSACTION;

-- TABLES

CREATE TABLE IF NOT EXISTS project (
	id integer primary key,
	project_name varchar(255),
	git_repo_path varchar(255)
);


CREATE TABLE IF NOT EXISTS issue (
	id integer primary key,
	project_id integer default 0,
	opener_id integer,
	assignee_id integer,
	opener_name varchar(255),
	assignee_name varchar(255),
	category_id integer default 0;
	status integer,
	title text,
	content text,
	priority integer,
	milestone_id integer,
	create_date datetime
);


CREATE TABLE IF NOT EXISTS issue_attachments (
	id integer primary key,
	issue_id integer,
	filename varchar(255)
);


CREATE TABLE IF NOT EXISTS issue_update (
	id integer primary key,
	issue_id integer,
	user_id integer,
	old_assignee integer,
	new_assignee integer,
	old_category integer default 0,
	new_category integer default 0,
	old_status integer,
	new_status integer,
	old_priority integer,
	new_priority integer,
	old_milestone integer,
	new_milestone integer,
	content text,
	create_date datetime
);


CREATE TABLE IF NOT EXISTS milestone (
	id integer primary key,
	milestone_name varchar(255),
	milestone_status integer default 0,
	project_id integer default 0,
	due_date datetime
);


CREATE TABLE IF NOT EXISTS category (
	id integer primary key,
	category_name varchar(255),
	project_id integer default 0,
	default_assignee_id integer
);


CREATE TABLE IF NOT EXISTS sessions (
    session_id char(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL default current_timestamp,
    data text
);


CREATE TABLE IF NOT EXISTS user (
	id integer primary key,
	username varchar(255),
	password varchar(255),
	email varchar(255)
);




-- TRIGGERS

CREATE TRIGGER IF NOT EXISTS insert_issue_create_date AFTER INSERT ON issue
BEGIN
	UPDATE issue SET create_date = datetime('now') WHERE rowid = new.rowid;
	UPDATE issue SET opener_name = (SELECT username FROM user WHERE id=new.opener_id);
END;


CREATE TRIGGER IF NOT EXISTS insert_issue_update_create_date AFTER INSERT ON issue_update
BEGIN
	UPDATE issue_update SET create_date = datetime('now')
	WHERE rowid = new.rowid;
END;


CREATE TRIGGER IF NOT EXISTS update_user_change_usernames AFTER UPDATE ON user
BEGIN
	UPDATE issue SET opener_name=new.username WHERE opener_id=new.id;
	UPDATE issue SET assignee_name=new.username WHERE assignee_id=new.id;
END;




-- VIEWS

CREATE VIEW IF NOT EXISTS issue_view AS
SELECT * FROM
  issue
JOIN
  milestone ON issue.milestone_id=milestone.id;


CREATE VIEW IF NOT EXISTS issue_update_view AS
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

