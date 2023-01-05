// npm run devStart

const express = require('express')
const session = require('express-session')
const flash = require('express-flash')
const bcrypt = require('bcrypt')
const bodyParser = require('body-parser')
const path = require('path')
const passport = require('passport')
const { user } = require('pg/lib/defaults')
const { client } = require('./dbConfig') 

var loginId = null

client.connect().then(() => {
    console.log('Successfully connected to the database');
}).catch(err => {
    console.error('Failed to connect to the database', err.stack);
});

const app = express()

const initializePassport = require('./passportConfig')

initializePassport(passport)

// Set static files
app.set('view engine', 'ejs')
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.urlencoded({ extended: false}))
app.use(bodyParser.json())
app.use(session({
    secret: 'secret',
    resave: false,
    saveUninitialized: false
}))
app.use(passport.initialize())
app.use(passport.session())
app.use(flash())


// Route for /
app.get('/', (req, res) => {
    res.render('dashboard')
}) 

// Route for index
app.get('/login', checkAuthenticated, (req, res) => {
    res.render('login')
})

app.get('/logout', (req, res, next)=>{
    console.log('Requesting logout...')
    req.logout(function(err) {
        if (err) { return next(err)}
        req.flash('sucess_msg', "You have been logged out")
        console.log("Id logged out:", loginId)
        loginId = null
        console.log("Id now: ", loginId)
        console.log('Logout successful!')
        res.redirect('/login')
      })
})

app.get('/dashboard', checkNotAuthenticated, (req, res)=>{
    sql = 'SELECT c.course_id, c.course_code, c.course_name, c.schedule, c.credit, c.weekly_hours, c.lecturer, g.category_name FROM courses c, student_courses s, students i, course_category g WHERE c.course_id = s.course_id AND s.student_id = i.id AND i.student_id = $1 AND c.course_type = g.course_type'
    
    params = [loginId]
    var courses = null
    var flag = false
    console.log("Login id is: ", loginId)
    client.query(sql, params, (err, result)=>{
        if (err) {throw err}
        courses = result.rows
        console.log('Courses:')
        // courses.forEach(row => {
        //     console.log(`- ${row.course_name}`);
        // })
        flag = true
        res.render('dashboard', {courses: courses})
    })
})

app.get('/info', (req, res)=>{
    res.render('info')
})

app.get('/general-course-recommendation', checkNotAuthenticated, (req, res)=>{
    sql = 'SELECT c.course_id, c.course_code, c.course_name, c.schedule, c.credit, c.weekly_hours, c.lecturer, c.likes FROM courses c WHERE c.course_id NOT IN (SELECT sc.course_id FROM student_courses sc WHERE sc.student_id = $1) ORDER BY c.likes DESC LIMIT 10'
    params = [loginId]

    console.log("Login id is: ", loginId)
    client.query(sql, params, (err, result)=>{
        if (err) {throw err}
        const courses = result.rows
        console.log('Courses:')
        // courses.forEach(row => {
        //     console.log(`- ${row.course_name}`);
        // })
        flag = true
        res.render('general-course-recommendation', {courses: courses})
    })
})

app.get('/required-course-recommendation', checkNotAuthenticated, (req, res)=>{
    sql = 'SELECT DISTINCT c.course_id, c.course_code, c.course_name, c.schedule, c.credit, c.weekly_hours, c.lecturer, c.likes FROM courses c, major_requirements m JOIN students s ON m.department_id = s.department_id LEFT JOIN student_courses sc ON sc.student_id = s.student_id WHERE s.student_id = $1 AND sc.student_id IS NULL AND m.course_name = SUBSTR(c.course_name, 1, LENGTH(m.course_name)) ORDER BY c.likes DESC, c.course_name ASC;'
    params = [loginId]

    console.log("Login id is: ", loginId)
    client.query(sql, params, (err, result)=>{
        if (err) {throw err}
        const courses = result.rows
        console.log('Courses:')
        // courses.forEach(row => {
        //     console.log(`- ${row.course_name}`);
        // })
        flag = true
        res.render('required-course-recommendation', {courses: courses})
    })
})


app.get('/must-take', checkNotAuthenticated, (req, res)=>{
    sql = 'SELECT m.course_name, m.year, m.semester FROM major_requirements m JOIN students s ON m.department_id = s.department_id LEFT JOIN student_courses sc ON sc.student_id = s.student_id WHERE s.student_id = $1 AND sc.student_id IS NULL'
    params = [loginId]
    
    console.log("Login id is: ", loginId)
    client.query(sql, params, (err, result)=>{
        if (err) {throw err}
        const courses = result.rows
        console.log('Courses:')
        // courses.forEach(row => {
        //     console.log(`- ${row.course_name}`);
        // })
        flag = true
        res.render('must-take', {courses: courses})
    })
})



app.get('/insert_values', (req, res)=>{
    res.render('insert_values')
})

app.get('/insert_user_data', (req, res)=>{
    res.render('insert_user_data', {name: '', cname: ''})
})

app.post('/insert-value', (req, res)=>{
    const studentId = req.body.username
    const password = req.body.password
    
    bcrypt.hash(password, 10, (err, hash) =>{
        if (err) {throw err}

        const sql = 'INSERT INTO users(student_id, student_password) VALUES ($1, $2)'
        const params = [studentId, hash]

        console.log(studentId, password)
        client.query(sql, params, (err, res) =>{
            if (err) {throw err}
            console.log("Successfully insert the following values: ", studentId, password, hash)
        })
    })

    res.redirect('insert_values')
})

app.post('/insert-user-data', (req, res)=>{
    const studentId = req.body.username
    const name = req.body.name
    const cname = req.body.cname
    const did = req.body.did
    const grade = req.body.grade
    const semester = req.body.semester
    console.log("Values to insert: ", studentId, name, cname, did, grade, semester)
    const sql = 'INSERT INTO students(student_id, name, chinese_name, department_id, grade, semester) VALUES($1, $2, $3, $4, $5, $6)'
    const params = [studentId, name, cname, did, grade, semester]


    client.query('SELECT department_id FROM departments', (err, res)=>{
        if (err) {throw err}
        const data = res.rows
        var exist = false

        data.forEach(row =>{
            if (row.department_id === did){
                exist = true
            }
        })

        if (exist){
            client.query(sql, params, (err, res) =>{
                if (err) {throw err}
                console.log("Successfully insert the following values: ", studentId, name, cname, did, grade, semester)
            })
        } else {
            console.log('Wrong Department ID!')
        }
    })
    res.redirect('/insert_user_data')
    
})

app.get('/query_user_data', (req, res)=>{
    client.query('SELECT * FROM students', (err, res)=>{
        const data = res.rows;

        console.log('Data:');
        data.forEach(row => {
            console.log(`Id: ${row.student_id} Name: ${row.student_name} Chinese Name: ${row.c_name}`);
        })
    })
})

// Route for login
app.post('/log-in', (req, res, next)=>{
    const authen = passport.authenticate('local', {
        successRedirect: '/dashboard',
        failureRedirect: '/login',
        failureFlash: true
    })

    loginId = req.body.username
    console.log("The user logged in is: ", loginId) 

    authen(req, res, next)
})


function checkAuthenticated(req, res, next) {
    if (req.isAuthenticated()) {
      return res.redirect("/dashboard");
    }
    next();
  }
  
function checkNotAuthenticated(req, res, next) {
    if (req.isAuthenticated()) {
        return next();
    }

    res.redirect("/login");
}

app.listen(3000)