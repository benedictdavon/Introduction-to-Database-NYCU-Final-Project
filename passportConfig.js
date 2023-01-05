const LocalStrategy = require('passport-local').Strategy
const { client } = require('./dbConfig')
const bcrypt = require('bcrypt')

function initialize(passport){
    console.log("initialized!")

    const authenticateUser = (student_id, password, done) => {
        // console.log(student_id, password)

        client.query(
            `SELECT * FROM users WHERE student_id = $1`, 
            [student_id], 
            (err, results)=>{
                if (err) {throw err}
                if (results.rows.length === 0){
                    // Incorect Student ID
                    return done(null, false, {message:"Incorect Student ID!"})
                }

                const user = results.rows[0]
                bcrypt.compare(password, user.student_password, (err, isMatch) => {
                    if (err) {throw err}
                    // Password correct
                    // console.log(password, user.student_password)
                    if (isMatch){
                        return done(null, user)
                    } else {
                        // Incorect password
                        return done(null, false, {message:"Incorrect Password!"})
                    }
                })                   
        })
    }

    passport.use(new LocalStrategy({
        usernameField: "username", passwordField: "password"
    }, authenticateUser))

    passport.serializeUser((user, done)=>done(null, user.student_id))

    passport.deserializeUser((student_id, done)=>{
        client.query(
            `SELECT * FROM users WHERE student_id = $1`, [student_id], (err, results)=>{
                // console.log('Deserializing')
                if (err) {throw err}
                // console.log('Id is: ', results.rows[0])
                return done(null, results.rows[0])
            }
        )
    })
}

module.exports = initialize