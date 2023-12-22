from flask import Flask, render_template, url_for,request,redirect,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
from passlib.hash import sha256_crypt


app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = 'komikstore'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'sql12.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql12671859'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = '43mqN4tAK9'
app.config['MYSQL_DB'] = 'sql12671859'

mysql = MySQL(app)

def perform_login(username, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_data WHERE username = %s AND password = %s", (username, password,))
    user_data = cur.fetchone()
    cur.close()

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
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_data WHERE email = %s AND password = %s', (email, password,))
        # Fetch one record and return the result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect email/password!'
    return render_template('login.html', msg='')

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
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
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
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('INSERT INTO user_data (id, email, username, password) VALUES (NULL, %s, %s, %s)', (email, username, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered! now u can login'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    # Check if account exists using MySQL
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
