DROP TABLE IF EXISTS User;
CREATE TABLE User (
    user_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(40) NOT NULL,
    password CHAR(100) NOT NULL,
    age INTEGER,
    major VARCHAR(100)
);

DROP TABLE IF EXISTS Class;
CREATE TABLE Class (
    class_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    class_major VARCHAR(100) NOT NULL,
    class_name VARCHAR(100) NOT NULL,
    credit_hours INTEGER
);

DROP TABLE IF EXISTS Review;
CREATE TABLE Review (
    user_id INTEGER,
    class_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    date_posted DATE NOT NULL,
    description VARCHAR(500),
    title VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES Class(class_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS Professor;
CREATE TABLE Professor (
    professor_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    professor_name VARCHAR(50) NOT NULL
);

DROP TABLE IF EXISTS University;
CREATE TABLE University (
    university_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    university_name VARCHAR(50) NOT NULL,
    state CHAR(2),
    type VARCHAR(100)
);

-- Students have taken what class
DROP TABLE IF EXISTS Taken;
CREATE TABLE Taken (
    user_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, class_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES Class(class_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Users post what reviews (relation to class)
DROP TABLE IF EXISTS Posts;
CREATE TABLE Posts (
    user_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, class_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES Class(class_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Professor has what reviews
DROP TABLE IF EXISTS Has;
CREATE TABLE Has (
    professor_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (professor_id, user_id),
    FOREIGN KEY (professor_id) REFERENCES Professor(professor_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Teacher teaches what class
DROP TABLE IF EXISTS Teaches;
CREATE TABLE Teaches (
    professor_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    PRIMARY KEY (professor_id, class_id),
    FOREIGN KEY (professor_id) REFERENCES Professor(professor_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES Class(class_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Class is taught at what university
DROP TABLE IF EXISTS Taught_At;
CREATE TABLE Taught_At (
    class_id INTEGER NOT NULL,
    university_id INTEGER NOT NULL,
    PRIMARY KEY (class_id, university_id),
    FOREIGN KEY (class_id) REFERENCES Class(class_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (university_id) REFERENCES University(university_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Professor teaches at what university
DROP TABLE IF EXISTS Teaches_At;
CREATE TABLE Teaches_At (
    professor_id INTEGER NOT NULL,
    university_id INTEGER NOT NULL,
    PRIMARY KEY (professor_id, university_id),
    FOREIGN KEY (professor_id) REFERENCES Professor(professor_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (university_id) REFERENCES University(university_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);





-- Insertions Operations
INSERT INTO University(university_name, state, type) VALUES
    ("Missouri University of Science and Technology", "MO", "Co-Education"),
    ("University of Missouri", "MO", "Co-Education"),
    ("Hampden-Sydney College", "VA", "Male Only");

INSERT INTO Class(class_major, class_name, credit_hours) VALUES 
    ("Computer Science", "Comp Sci-2300", 3),
    ("Computer Science", "Comp Sci 3800", 3),
    ("Civil Engineering", "CV ENG 1000", 1),
    ("Data Science", "Data Sci-1030", 3),
    ("English", "English 337", 3),
    ("English", "English 481", 1);

INSERT INTO Professor(professor_name) VALUES 
    ("Dr. Josh Wilkerson"), 
    ("San Yeung"), 
    ("James Garl"), 
    ("Chris Don"), 
    ("Dr. Connor Jones");

INSERT INTO Teaches_At(professor_id, university_id) VALUES
    (1,1), (2, 1), (3,2), (4,2), (5,3);

INSERT INTO Teaches(professor_id, class_id) VALUES
    (1, 2), (2, 1), (3, 3), (4, 4), (5, 5), (5, 6);
    
INSERT INTO Taught_At(class_id, university_id) VALUES
	(1, 1), (2, 1), (3, 2), (4, 2), (5, 3), (6, 3);
    
INSERT INTO User(username, password, age, major) VALUES
	("njp1", "njp1", 21, "Computer Science"),
    ("njp2", "njp2", 22, "Civil Engineering"),
    ("njp3", "njp3", 25, "English Literature"),
    ("njp4", "njp4", 19, "Mechanical Engineering");
    
INSERT INTO Review(user_id, class_id, rating, date_posted, description, title) VALUES
	(1, 6, 10, "2015-09-09", "It's an easy English class", "Easy class"),
    (1, 2, 10, "2025-12-12", "100% would recommned", "Take it"),
    (1, 1, 8, "2025-11-28", "Teacher is good but class is hard", "Take at your own risk"),
    (1, 3, 5, "1909-09-23", "Took it 100 years ago but it was bad", "Don't take if it still exists"),
    (1, 5, 7, "2015-03-04", "It was alright but pretty boring", "Decent choice"),
    (2, 1, 5, "1808-09-09", "Never even took the class", "Don't take"),
    (2, 3, 10, "2020-12-20", "Didn't even attend class and got an A", "Free A"),
    (3, 2, 7, "2020-07-21", "classes were always on zoom butit was fine", "Okay class"),
    (3, 4, 4, "2023-09-19", "It was horrible", "Pass on it");

INSERT INTO Taken(user_id, class_id) VALUES
	(1, 6),
    (1, 2),
    (1, 1),
    (1, 3),
    (1, 5),
    (2, 1),
    (2, 3), 
    (3, 2), 
    (3, 4);

INSERT INTO Posts(user_id, class_id) VALUES
	(1, 6),
    (1, 2),
    (1, 1),
    (1, 3),
    (1, 5),
    (2, 1),
    (2, 3), 
    (3, 2), 
    (3, 4);
   
INSERT INTO Has(professor_id, user_id) VALUES
	(5, 1),
    (1, 1),
    (2, 1),
    (3, 1),
    (2, 2),
    (3, 2), 
    (1, 3), 
    (4, 3);    