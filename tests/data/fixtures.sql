PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (user_id integer primary key autoincrement, username text);
INSERT INTO users VALUES(1,'mcfunley');
INSERT INTO users VALUES(2,'oscar');
INSERT INTO users VALUES(3,'dottie');
COMMIT;
