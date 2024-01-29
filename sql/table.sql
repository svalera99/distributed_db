CREATE TABLE user_counter(
    user_id INTEGER PRIMARY KEY, 
    counter INTEGER,
    version INTEGER 
);

INSERT INTO user_counter(user_id, counter, version)
VALUES (1, 0, 0);