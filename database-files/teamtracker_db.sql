DROP DATABASE IF EXISTS teamTracker;
CREATE DATABASE IF NOT EXISTS teamTracker;
USE teamTracker;


DROP TABLE IF EXISTS StrategyEvent;
DROP TABLE IF EXISTS StatEvent;
DROP TABLE IF EXISTS PlayerEvent;
DROP TABLE IF EXISTS Injury;
DROP TABLE IF EXISTS Comment;
DROP TABLE IF EXISTS Event;
DROP TABLE IF EXISTS Strategy;
DROP TABLE IF EXISTS Coach;
DROP TABLE IF EXISTS Analyst;
DROP TABLE IF EXISTS Admin;
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Team;


DROP TABLE IF EXISTS Team;
CREATE TABLE IF NOT EXISTS Team
(
   teamID      INTEGER PRIMARY KEY AUTO_INCREMENT,
   teamName    VARCHAR(120)NOT NULL,
   teamColor   VARCHAR(50)
);




DROP TABLE IF EXISTS Players;
CREATE TABLE IF NOT EXISTS Players
(
   playerID      INTEGER PRIMARY KEY AUTO_INCREMENT,
   name          VARCHAR(120) NOT NULL,
   position      VARCHAR(50),
   gradYear      INTEGER,
   phoneNumber   VARCHAR(30),
   jerseyNumber  INTEGER,
   teamID        INTEGER NOT NULL,

   FOREIGN KEY (teamID)
       REFERENCES Team(teamID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT
);




DROP TABLE IF EXISTS Admin;
CREATE TABLE IF NOT EXISTS Admin
(
   adminID      INTEGER PRIMARY KEY AUTO_INCREMENT,
   name         VARCHAR(100) NOT NULL,
   email        VARCHAR(150) NOT NULL UNIQUE,
   phoneNumber  VARCHAR(30),
   teamID       INTEGER NOT NULL,


   FOREIGN KEY (teamID)
       REFERENCES Team(teamID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT
);




DROP TABLE IF EXISTS Analyst;
CREATE TABLE IF NOT EXISTS Analyst
(
   analystID     INTEGER PRIMARY KEY AUTO_INCREMENT,
   name          VARCHAR(120) NOT NULL,
   email         VARCHAR(150) NOT NULL UNIQUE,
   phoneNumber   VARCHAR(30),
   teamID        INTEGER NOT NULL,


   FOREIGN KEY (teamID)
       REFERENCES Team(teamID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT
);




DROP TABLE IF EXISTS Coach;
CREATE TABLE IF NOT EXISTS Coach
(
   coachID      INTEGER PRIMARY KEY AUTO_INCREMENT,
   name         VARCHAR(120) NOT NULL,
   email        VARCHAR(150) NOT NULL UNIQUE,
   phoneNumber  VARCHAR(30),
   teamID       INTEGER NOT NULL,


   FOREIGN KEY (teamID)
       REFERENCES Team(teamID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT
);




DROP TABLE IF EXISTS Strategy;
CREATE TABLE IF NOT EXISTS Strategy
(
   strategyID   INTEGER PRIMARY KEY AUTO_INCREMENT,
   formation    VARCHAR(80) NOT NULL,
   coachID      INTEGER NOT NULL,


   FOREIGN KEY (coachID)
       REFERENCES Coach(coachID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT
);




DROP TABLE IF EXISTS Event;
CREATE TABLE IF NOT EXISTS Event
(
   eventID     INTEGER PRIMARY KEY AUTO_INCREMENT,
   location    VARCHAR(150),
   dateTime    DATETIME NOT NULL,
   teamID      INTEGER NOT NULL,


   FOREIGN KEY (teamID)
       REFERENCES Team(teamID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT
);




DROP TABLE IF EXISTS PlayerEvent;
CREATE TABLE IF NOT EXISTS PlayerEvent
(
   eventID    INTEGER,
   playerID   INTEGER,
   PRIMARY KEY (eventID, playerID),


   FOREIGN KEY (eventID)
       REFERENCES Event(eventID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT,


   FOREIGN KEY (playerID)
       REFERENCES Players(playerID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT
);




DROP TABLE IF EXISTS StatEvent;
CREATE TABLE IF NOT EXISTS StatEvent
(
   statID     INTEGER PRIMARY KEY AUTO_INCREMENT,
   dateTime   DATETIME NOT NULL,
   statType   VARCHAR(80) NOT NULL,
   eventID    INTEGER NOT NULL,
   playerID   INTEGER NOT NULL,


   FOREIGN KEY (eventID)
       REFERENCES Event(eventID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT,


   FOREIGN KEY (playerID)
       REFERENCES Players(playerID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT
);




DROP TABLE IF EXISTS Injury;
CREATE TABLE IF NOT EXISTS Injury
(
   injuryID      INTEGER PRIMARY KEY AUTO_INCREMENT,
   type          VARCHAR(120) NOT NULL,
   date          DATE NOT NULL,
   recoveryDate  DATE,
   playerID      INTEGER NOT NULL,


   FOREIGN KEY (playerID)
       REFERENCES Players(playerID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT
);




DROP TABLE IF EXISTS Comment;
CREATE TABLE IF NOT EXISTS Comment
(
   commentID     INTEGER PRIMARY KEY AUTO_INCREMENT,
   text          TEXT NOT NULL,
   dateTime      DATETIME NOT NULL,
   commenterID   INTEGER NOT NULL,
   targetID      INTEGER NOT NULL,


   FOREIGN KEY (commenterID)
       REFERENCES Analyst(analystID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT,


   FOREIGN KEY (targetID)
       REFERENCES Players(playerID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT
);




DROP TABLE IF EXISTS StrategyEvent;
CREATE TABLE IF NOT EXISTS StrategyEvent
(
   strategyID   INTEGER,
   eventID      INTEGER,
   result       varchar(10) NOT NULL,
   PRIMARY KEY (strategyID, eventID),


   FOREIGN KEY (strategyID)
       REFERENCES Strategy(strategyID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT,


   FOREIGN KEY (eventID)
       REFERENCES Event(eventID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT
);

# Teams
INSERT INTO Team (teamName, teamColor) VALUES ('Northeastern FC', 'Red');
INSERT INTO Team (teamName, teamColor) VALUES ('Boston United', 'Blue');
INSERT INTO Team (teamName, teamColor) VALUES ('Cambridge City', 'Black');

# Players
INSERT INTO Players (name, position, gradYear, phoneNumber, jerseyNumber, teamID)
VALUES ('Freddy Elyas', 'Midfielder', 2026, '617-555-1111', 8, 1);

INSERT INTO Players (name, position, gradYear, phoneNumber, jerseyNumber, teamID)
VALUES ('Marc Sawaya', 'Goalkeeper', 2025, '617-555-2222', 1, 1);

INSERT INTO Players (name, position, gradYear, phoneNumber, jerseyNumber, teamID)
VALUES ('Carter Anderson', 'Forward', 2027, '617-555-3333', 11, 1);

# Admin
INSERT INTO Admin (name, email, phoneNumber, teamID)
VALUES ('Susan Howard', 'susan.howard@northeastern.edu', '617-555-4444', 1);

INSERT INTO Admin (name, email, phoneNumber, teamID)
VALUES ('Tom Green', 't.green@bostonunited.com', '617-555-5555', 2);

INSERT INTO Admin (name, email, phoneNumber, teamID)
VALUES ('Maria Ortiz', 'm.ortiz@cambridgecity.com', '617-555-6666', 3);

# Analyst 
INSERT INTO Analyst (name, email, phoneNumber, teamID)
VALUES ('John Analyst', 'john.analyst@northeastern.edu', '617-555-7777', 1);

INSERT INTO Analyst (name, email, phoneNumber, teamID)
VALUES ('Sarah Metrics', 's.metrics@bostonunited.com', '617-555-8888', 2);

INSERT INTO Analyst (name, email, phoneNumber, teamID)
VALUES ('Ben Carter', 'ben.c@cambridgecity.com', '617-555-9999', 3);

# Coach 
INSERT INTO Coach (name, email, phoneNumber, teamID)
VALUES ('Coach Riley', 'riley@northeastern.edu', '617-555-1010', 1);

INSERT INTO Coach (name, email, phoneNumber, teamID)
VALUES ('Coach Mills', 'mills@bostonunited.com', '617-555-2020', 2);

INSERT INTO Coach (name, email, phoneNumber, teamID)
VALUES ('Coach Alvarez', 'alvarez@cambridgecity.com', '617-555-3030', 3);

# Strategy 
INSERT INTO Strategy (formation, coachID) VALUES ('4-4-2', 1);
INSERT INTO Strategy (formation, coachID) VALUES ('4-3-3', 1);
INSERT INTO Strategy (formation, coachID) VALUES ('3-5-2', 1);

# Event 
INSERT INTO Event (location, dateTime, teamID)
VALUES ('Carter Field', '2025-11-16 14:00:00', 1);

INSERT INTO Event (location, dateTime, teamID)
VALUES ('Carter Field', '2025-11-18 18:30:00', 1);

INSERT INTO Event (location, dateTime, teamID)
VALUES ('Cambridge Center', '2025-11-20 17:00:00', 1);

# PlayerEvent 
INSERT INTO PlayerEvent (eventID, playerID) VALUES (1, 1);
INSERT INTO PlayerEvent (eventID, playerID) VALUES (1, 2);
INSERT INTO PlayerEvent (eventID, playerID) VALUES (2, 1);

# StatEvent 
INSERT INTO StatEvent (dateTime, statType, eventID, playerID)
VALUES ('2025-11-16 16:05:00', 'goal', 1, 3);

INSERT INTO StatEvent (dateTime, statType, eventID, playerID)
VALUES ('2025-11-16 16:06:00', 'assist', 1, 1);

INSERT INTO StatEvent (dateTime, statType, eventID, playerID)
VALUES ('2025-11-18 19:20:00', 'save', 2, 2);

# Injury 
INSERT INTO Injury (type, date, recoveryDate, playerID)
VALUES ('ACL tear', '2025-10-01', '2026-03-01', 2);

INSERT INTO Injury (type, date, recoveryDate, playerID)
VALUES ('Hamstring strain', '2025-11-02', '2025-11-20', 3);

INSERT INTO Injury (type, date, recoveryDate, playerID)
VALUES ('Concussion', '2025-09-14', NULL, 1);

# Comment 
INSERT INTO Comment (text, dateTime, commenterID, targetID)
VALUES ('Solid performance today.', NOW(), 1, 1);

INSERT INTO Comment (text, dateTime, commenterID, targetID)
VALUES ('Needs improvement on defense.', NOW(), 1, 3);

INSERT INTO Comment (text, dateTime, commenterID, targetID)
VALUES ('Excellent leadership.', NOW(), 1, 2);

# StrategyEvent 
INSERT INTO StrategyEvent (strategyID, eventID, result)
VALUES (1, 1, 'WIN');

INSERT INTO StrategyEvent (strategyID, eventID, result)
VALUES (2, 2, 'LOSS');

INSERT INTO StrategyEvent (strategyID, eventID, result)
VALUES (3, 3, 'DRAW');