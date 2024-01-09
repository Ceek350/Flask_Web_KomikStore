from flask import Flask, render_template, url_for, request, redirect, session, jsonify
import mysql.connector
import re
import hashlib
from passlib.hash import sha256_crypt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = 'komikstore'

# Create a connection to your MySQL database
mydb = mysql.connector.connect(
    host='sql.freedb.tech',
    user='freedb_zerostore',
    port=3306,
    password='9XcMJypct#5tX&J',
    database='freedb_zerostore'
)

@app.route('/')
def anu():
    return render_template('index.html', user=None)

@app.route('/home')
def dashboard():
    username = None
    if 'username' in session:
        return render_template('index.html', username, user=session['username'])
    else:
        return redirect('/logindb')

@app.route('/logindb', methods=['GET', 'POST'])
def logindb():
    user = None
    error = ''  # Variabel untuk menyimpan pesan error

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mydb.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user_data WHERE username = %s and password = %s', (username, password))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect('/home', username, user=session['username'])
        else:
            error = 'Invalid username or password'

    return render_template('index.html', error=error, user=user)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

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


#API User
@app.route('/user', methods=['GET'], endpoint='v1')
def get_users():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM user_data")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)

#API post
#API Comment


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
