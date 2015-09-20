BEGIN;

DROP DATABASE project;
CREATE DATABASE project;
USE project;

-- TABLES

CREATE TABLE IF NOT EXISTS project (
	id INT NOT NULL AUTO_INCREMENT,
	project_name varchar(255),
	git_repo_path varchar(255),
	PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS issue (
	id INT NOT NULL AUTO_INCREMENT,
	project_id integer default 0,
	opener_id integer,
	assignee_id integer,
	opener_name varchar(255),
	assignee_name varchar(255),
	category_id integer default 0,
	status integer,
	title text,
	content text,
	priority integer,
	milestone_id integer,
	create_date datetime,
	PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS issue_attachments (
	id INT NOT NULL AUTO_INCREMENT,
	issue_id integer,
	filename varchar(255),
	PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS issue_update (
	id INT NOT NULL AUTO_INCREMENT,
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
	create_date datetime,
	PRIMARY KEY (id)
);


CREATE TABLE user_filter (
	id INT NOT NULL AUTO_INCREMENT,
	user_id integer,
	filter VARCHAR(255),
	PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS milestone (
	id INT NOT NULL AUTO_INCREMENT,
	milestone_name varchar(255),
	milestone_status integer default 0,
	project_id integer default 0,
	due_date datetime,
	PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS category (
	id INT NOT NULL AUTO_INCREMENT,
	category_name varchar(255),
	project_id integer default 0,
	default_assignee_id integer,
	PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS sessions (
    session_id char(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL default current_timestamp,
    data text
);


CREATE TABLE IF NOT EXISTS user (
	id INT NOT NULL AUTO_INCREMENT,
	username varchar(255),
	password varchar(255),
	email varchar(255),
	PRIMARY KEY (id)
);

COMMIT;

-- FUNCTIONS

DELIMITER $$

DROP FUNCTION IF EXISTS username_from_id $$

CREATE FUNCTION username_from_id(userid INT) RETURNS varchar(255)
BEGIN
	DECLARE un varchar(255);
	SELECT username INTO un FROM user WHERE id=userid;
	RETURN un;
END $$

DELIMITER ;

-- TRIGGERS

BEGIN;

DELIMITER $$

DROP TRIGGER IF EXISTS insert_issue_create_date $$

CREATE TRIGGER insert_issue_create_date BEFORE INSERT ON issue
FOR EACH ROW
BEGIN
	SET NEW.create_date = NOW();
	SET NEW.opener_name = username_from_id(NEW.opener_id);
END $$


DROP TRIGGER IF EXISTS insert_issue_update_create_date $$

CREATE TRIGGER insert_issue_update_create_date BEFORE INSERT ON issue_update
FOR EACH ROW
BEGIN
	SET NEW.create_date = NOW();
END $$


DROP TRIGGER IF EXISTS update_user_change_usernames $$

CREATE TRIGGER update_user_change_usernames BEFORE UPDATE ON user
FOR EACH ROW
BEGIN
	UPDATE issue SET opener_name=NEW.username WHERE opener_id=NEW.id;
	UPDATE issue SET assignee_name=NEW.username WHERE assignee_id=NEW.id;
END $$

DELIMITER ;

COMMIT;


-- VIEWS

BEGIN;

CREATE VIEW issue_view AS
SELECT
	issue.id,
	issue.project_id,
	issue.opener_id,
	issue.assignee_id,
	issue.opener_name,
	issue.assignee_name,
	issue.category_id,
	issue.status,
	issue.title,
	issue.content,
	issue.priority,
	issue.milestone_id,
	issue.create_date,
	milestone.milestone_name,
	milestone.milestone_status, 
	milestone.due_date
FROM
  issue
JOIN
  milestone ON issue.milestone_id=milestone.id;


CREATE VIEW issue_update_view AS
SELECT
	issue_update.id,
	issue_update.issue_id,
	issue_update.user_id,
	issue_update.old_assignee,
	issue_update.new_assignee,
	issue_update.old_category,
	issue_update.new_category,
	issue_update.old_status,
	issue_update.new_status,
	issue_update.old_priority,
	issue_update.new_priority,
	issue_update.old_milestone,
	issue_update.new_milestone,
	issue_update.content,
	issue_update.create_date,
	user.username,
	user.email,
	old_ms.milestone_name as old_milestone_name,
	new_ms.milestone_name as new_milestone_name,
	old_cat.category_name as old_category_name,
	new_cat.category_name as new_category_name
FROM
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

