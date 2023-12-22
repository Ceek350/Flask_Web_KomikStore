from flask import Flask, render_template, url_for, request, redirect, session
import mysql.connector
import re
import hashlib
from passlib.hash import sha256_crypt

app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = 'komikstore'

# Create a connection to your MySQL database
mydb = mysql.connector.connect(
    host='sql12.freesqldatabase.com',
    user='sql12671859',
    port=3306,
    password='43mqN4tAK9',
    database='sql12671859'
)

def perform_login(username, password):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM user_data WHERE username = %s", (username,))
    user_data = mycursor.fetchone()
    mycursor.close()

    if user_data:
        hashed_password = user_data[3]
        if sha256_crypt.verify(password, hashed_password):
            return True
    return False

@app.route('/')
def anu():
    return render_template('index.html')

@app.route('/home')
def success_login():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('index.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
def index():
    return render_template('index.html')

@app.route('/logindb', methods=['GET', 'POST'])
def logindb():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Retrieve the hashed password
        hash_password = hashlib.sha1((password + app.secret_key).encode()).hexdigest()

        # Check if account exists using MySQL
        cursor = mydb.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user_data WHERE email = %s AND password = %s', (email, hash_password,))
        # Fetch one record and return the result
        account = cursor.fetchone()

        # If account exists in accounts table in our database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            # Redirect to home page or any other desired page
            return 'Logged in successfully!'
        else:
            # Account doesn't exist or username/password is incorrect
            msg = 'Incorrect email/password!'
    return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    # Redirect to login page
    return render_template('index.html')

@app.route('/registerdb', methods=['GET', 'POST'])
def registerdb():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        password = request.form['password']
        email = request.form['email']
        username = request.form['username']

        # Check if account exists using MySQL
        cursor = mydb.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user_data WHERE email = %s', (email,))
        account = cursor.fetchone()

        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Hash the password
            hash_password = hashlib.sha1((password + app.secret_key).encode()).hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('INSERT INTO user_data (id, email, username, password) VALUES (NULL, %s, %s, %s)', (email, username, hash_password,))
            mydb.commit()
            msg = 'You have successfully registered! Now you can login'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/about_us')
def about():
    return render_template("AboutUs.html")

if __name__== '__main__':
    app.run(debug=True)
