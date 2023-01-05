-- StudentID password     grade semester department_id
-- 110550199 notpassword  1     1        DCP
-- 110550200 ispassword   1     2        DCP
-- 110550201 password     2     1        DCP
-- 110550202 whatpassword 2     2        DCP
-- 110550203 pablopikachu 3     1        DCP
-- 110550204 choochoo     3     2        DCP
-- 110550205 water        4     1        DCP
-- 110550206 110550206    4     2        DCP


-- 1 for required, 2 for elective, 3 for core curiculum, 4 for physicial education, 5 for language and communication
CREATE TABLE course_category (
  course_type NUMERIC(1, 0),
  category_name VARCHAR(25),
  PRIMARY KEY (course_type)
);
INSERT INTO course_category(course_type, category_name) VALUES 
(1, 'Required'),
(2, 'Elective'),
(3, 'Core Curriculum'),
(4, 'Physical Education'),
(5, 'Language & Communication');

-- list the semester id and name, ex: 1111 = '111 Fall'
CREATE TABLE semesters(
  semester_id NUMERIC(4, 0),
  semester_name VARCHAR(255),
  PRIMARY KEY (semester_id)
);
INSERT INTO semesters(semester_id, semester_name) VALUES
(1111, '111 Fall'),
(1112, '111 Spring');

-- Information about the courses in NYCU
CREATE TABLE courses (
  semester_id NUMERIC(4, 0),
  course_id NUMERIC(6, 0),
  course_code VARCHAR(20),
  memo TEXT,
  course_name TEXT,
  chinese_name VARCHAR(255),
  reg_limit VARCHAR(10),
  reg_num NUMERIC(3, 0),
  schedule VARCHAR(100),
  credit NUMERIC(2, 1),
  weekly_hours NUMERiC(1),
  lecturer VARCHAR(255),
  course_type NUMERIC(1, 0),
  likes INT DEFAULT 0,
  PRIMARY KEY (course_id),
  FOREIGN KEY (course_type) REFERENCES course_category(course_type)
);

UPDATE courses SET likes = 342 WHERE course_id = 161001;
UPDATE courses SET likes = 67 WHERE course_id = 161002;
UPDATE courses SET likes = 112 WHERE course_id = 161003;
UPDATE courses SET likes = 445 WHERE course_id = 161004;
UPDATE courses SET likes = 207 WHERE course_id = 161005;
UPDATE courses SET likes = 755 WHERE course_id = 561006;
UPDATE courses SET likes = 310 WHERE course_id = 561029;
UPDATE courses SET likes = 591 WHERE course_id = 510004;
UPDATE courses SET likes = 1058 WHERE course_id = 510003;
UPDATE courses SET likes = 690 WHERE course_id = 561033;
UPDATE courses SET likes = 555 WHERE course_id = 561021;
UPDATE courses SET likes = 677 WHERE course_id = 310000;
UPDATE courses SET likes = 888 WHERE course_id = 515108;
UPDATE courses SET likes = 356 WHERE course_id = 517100;


-- Query what are the courses a student take this semester based on the login id
SELECT c.course_id, c.course_code, c.course_name, c.schedule, c.credit, c.weekly_hours, c.lecturer, g.category_name
FROM courses c, student_courses s, students i, course_category g
WHERE c.course_id = s.course_id AND s.student_id = i.id AND i.student_id = 110550201 AND c.course_type = g.course_type


\copy courses FROM 'C:\Users\Davon\Desktop\University\Semester 3\Introduction to Database System\Final Project\src\dataset\courses.csv' WITH (FORMAT CSV, HEADER)

-- List of college_name, department_id (ex: DCP, ECE), and department_name
CREATE TABLE departments (
  college_name VARCHAR(50),
  department_id VARCHAR(3),
  department_name VARCHAR(65),
  PRIMARY KEY(department_id)
);

\copy departments FROM 'C:/Users/Davon/Desktop/University/Semester 3/Introduction to Database System/Final Project/src/dataset/colleges.csv' WITH (FORMAT CSV, HEADER)

-- List of what are the courses a student from a department must take during their study
CREATE TABLE major_requirements (
  id SERIAL,
  department_id VARCHAR(3),
  course_name VARCHAR(255),
  year NUMERIC(1, 0),
  semester NUMERIC(1, 0),
  PRIMARY KEY (id),
  FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

SELECT c.course_id, c.course_code, c.course_name, c.schedule, c.credit, c.weekly_hours, c.lecturer, c.likes
FROM courses c
WHERE c.course_id NOT IN (SELECT sc.course_id FROM student_courses sc WHERE sc.student_id = 110550201)
ORDER BY c.likes DESC;

-- Query the courses from courses table a student haven't take
SELECT DISTINCT c.course_id, c.course_code, c.course_name, c.lecturer, c.likes
FROM courses c, major_requirements m
JOIN students s ON m.department_id = s.department_id
LEFT JOIN student_courses sc ON sc.student_id = s.student_id
WHERE s.student_id = 110550201 AND sc.student_id IS NULL AND m.course_name = SUBSTR(c.course_name, 1, LENGTH(m.course_name))
ORDER BY c.likes DESC, c.course_name ASC;

-- Query the courses from major_requirements a student haven't take
SELECT m.course_name, m.year, m.semester
FROM major_requirements m
JOIN students s ON m.department_id = s.department_id
LEFT JOIN student_courses sc ON sc.student_id = s.student_id
WHERE s.student_id = 110550201 AND sc.student_id IS NULL


INSERT INTO major_requirements(department_id, course_name, year, semester) VALUES
('DCP', 'Physical Education', 1, 1),
('DCP', 'Physical Education', 1, 2),
('DCP', 'Physical Education', 2, 1),
('DCP', 'Physical Education', 2, 2),
('DCP', 'Physical Education', 3, 1),
('DCP', 'Physical Education', 3, 2),
('DCP', 'Service Learning (I)', 1, 2),
('DCP', 'Service Learning (II)', 2, 1),
('DCP', 'Career Planning and Mentor''s Hours ', 1, 1),
('DCP', 'Career Planning and Mentor''s Hours ', 1, 2),
('DCP', 'Physics (I)', 1, 1),
('DCP', 'Physics (II)', 1, 2),
('DCP', 'Calculus (I)', 1, 1),
('DCP', 'Calculus (II)', 1, 2),
('DCP', 'Linear Algebra', 1, 1),
('DCP', 'Introduction to Computers and Programming', 1, 1),
('DCP', 'Data Structures and Object-oriented Programming', 1, 2),
('DCP', 'Discrete Mathematics', 1, 2),
('DCP', 'Digital Circuit Design', 1, 2),
('DCP', 'Probability', 2, 1),
('DCP', 'Introduction to Algorithms', 2, 1),
('DCP', 'Basic Programming', 2, 2),
('DCP', 'Computer Organization', 2, 2),
('DCP', 'Introduction to Operating Systems', 3, 1),
('DCP', 'Computer Science Seminars', 3, 1),
('DCP', 'Computer Science and Engineering Projects (I)', 3, 2),
('DCP', 'Computer Science and Engineering Projects (II)', 3, 2);

-- The student data
CREATE TABLE students (
  id SERIAL,
  student_id NUMERIC(9, 0),
  name VARCHAR(255),
  chinese_name VARCHAR(255),
  department_id VARCHAR(3),
  grade INTEGER,
  semester INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY (department_id) REFERENCES departments(department_id),
  FOREIGN KEY (student_id) REFERENCES users(student_id)
);

INSERT INTO student_courses(student_id, course_id) VALUES 
(3, 563039), -- PE
(3, 563040), -- PE
(3, 510004), -- Statistic
(3, 515512), -- Intro to Algo
(3, 515514), -- Intro to DB
(3, 515605), -- Service Learning 2
(3, 515609), -- Basic Programming
(3, 563036); -- Swimming

-- What are the courses a student takes
CREATE TABLE student_courses (
  student_id INT,
  course_id NUMERIC(6, 0),
  PRIMARY KEY (student_id, course_id),
  FOREIGN KEY (student_id) REFERENCES students(id),
  FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
