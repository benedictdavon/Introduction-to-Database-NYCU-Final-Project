CREATE TABLE users(
    student_id NUMERIC(9, 0),
    student_password VARCHAR(255),
    PRIMARY KEY (student_id)
);


SET CLIENT_ENCODING TO 'UTF8';


INSERT INTO user_data(student_id, eng_name, ch_name) VALUES (110550201, 'Davon', '周恭麟');
INSERT INTO user_data(student_id, eng_name, ch_name) VALUES (109350082, 'Angel', '洪理詩');
INSERT INTO user_data(student_id, eng_name, ch_name) VALUES (109350000, 'oranges');
INSERT INTO user_data(student_id, eng_name, ch_name) VALUES (110550001, 'grapes');
INSERT INTO user_data(student_id, eng_name, ch_name) VALUES (110350111, 'notpassword');
INSERT INTO user_data(student_id, eng_name, ch_name) VALUES (110350222, 'thisispassword');
INSERT INTO user_data(student_id, eng_name, ch_name) VALUES (110350123, 'durian');
INSERT INTO user_data(student_id, eng_name, ch_name) VALUES (110550111, 'easypassword');
INSERT INTO user_data(student_id, eng_name, ch_name) VALUES (110550123, 'hardpassword');
INSERT INTO user_data(student_id, eng_name, ch_name) VALUES (110550124, 'pineaple');
INSERT INTO user_data(student_id, eng_name, ch_name) VALUES (110550125, 'angel');
INSERT INTO user_data(student_id, eng_name, ch_name) VALUES (110550126, 'devil');

INSERT INTO user_login(student_id, student_password) VALUES (1, '1');
INSERT INTO user_login(student_id, student_password) VALUES (110550201, 'password');
INSERT INTO user_login(student_id, student_password) VALUES (109350082, 'apple');
INSERT INTO user_login(student_id, student_password) VALUES (109350000, 'oranges');
INSERT INTO user_login(student_id, student_password) VALUES (110550001, 'grapes');
INSERT INTO user_login(student_id, student_password) VALUES (110350111, 'notpassword');
INSERT INTO user_login(student_id, student_password) VALUES (110350222, 'thisispassword');
INSERT INTO user_login(student_id, student_password) VALUES (110350123, 'durian');
INSERT INTO user_login(student_id, student_password) VALUES (110550111, 'easypassword');
INSERT INTO user_login(student_id, student_password) VALUES (110550123, 'hardpassword');
INSERT INTO user_login(student_id, student_password) VALUES (110550124, 'pineaple');
INSERT INTO user_login(student_id, student_password) VALUES (110550125, 'angel');
INSERT INTO user_login(student_id, student_password) VALUES (110550126, 'devil');

