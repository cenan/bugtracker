BEGIN TRANSACTION;

INSERT INTO milestone (milestone_name) VALUES ('Milestone 1');
INSERT INTO milestone (milestone_name) VALUES ('Milestone 2');
INSERT INTO milestone (milestone_name) VALUES ('Milestone 3');

INSERT INTO user (id, username, password) VALUES (1, 'admin', 'admin');

INSERT INTO category (id, category_name) VALUES (0, 'None');

COMMIT;

