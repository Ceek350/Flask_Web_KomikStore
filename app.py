from flask import Flask, render_template, url_for, request, redirect, session, jsonify
import mysql.connector
import re
import hashlib 
from hashlib import sha256
from passlib.hash import sha256_crypt
from werkzeug.security import generate_password_hash, check_password_hash


CLIENT_KEY = 'SB-Mid-client-Ay1WobiGTcJNoVKs'



app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = 'komikstore'
allowed_api_keys = ['abc123', '123abc']

def check_api_key(apiKey):
    return apiKey in allowed_api_keys

# Create a connection to your MySQL db
mydb = mysql.connector.connect(
    host='sql.freedb.tech',
    user='freedb_zerostore',
    port=3306,
    password='9XcMJypct#5tX&J',
    database='freedb_zerostore'
)

def initialize_database():
    # Placeholder for your actual MySQL database connection setup
    mydb = mysql.connector.connect(
    host='sql.freedb.tech',
    user='freedb_zerostore',
    port=3306,
    password='9XcMJypct#5tX&J',
    database='freedb_zerostore'
)
    return mydb

@app.route('/')
def anu():
    return render_template('index.html', user=None)

@app.route('/home')
def dashboard():
    user = None
    if 'email' in session:
        email = session['email']
        cursor = mydb.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user_data WHERE email = %s', (email,))
        user = cursor.fetchone()
        
        return render_template('index.html', user=user)
    else:
        return redirect('/login')

@app.route('/logindb', methods=['GET', 'POST'])
def logindb():
    # Output message if something goes wrong...
    msg = ''

    # Check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']

        # Check if the account exists using MySQL
        cursor = mydb.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user_data WHERE email = %s and password = %s', (email, password))
        account = cursor.fetchone()

        # If account exists, verify the password
        if account:
            session['email'] = email
            return redirect('/home')  # Redirect to the home page after successful login
        else:
            msg = 'Invalid email or password'

    # Show login form with message (if any)
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')

@app.route('/registerdb', methods=['GET', 'POST'])
def registerdb():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        
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
            # Hash the password using SHA-256
            hash_password = sha256((password + app.secret_key).encode()).hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('INSERT INTO user_data (id, email, password) VALUES (NULL, %s, %s)', (email, password,))
            mydb.commit()
            msg = 'You have successfully registered! Now you can login'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


#API KEY
@app.route('/api/api_key', methods=['GET'])
def api_key():
    return render_template("api_key.html")

#API User
@app.route('/api/data', methods=['GET'], endpoint='v1')
def get_users():
    apiKey = 'abc123'
    if not apiKey or not check_api_key(apiKey):
        return jsonify({'message': 'Unauthorized'}, 401)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM user_data where id")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)

@app.route('/api/user', methods=['GET'])
def get_user():
    apiKey = request.headers.get('apiKey')
    if not apiKey or not check_api_key(apiKey):
        return jsonify({'message': 'Unauthorized'}, 401)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM user_data where id")
    users = cursor.fetchall()
    cursor.close()
    return jsonify({'message': 'Data berhasil diambil'}, users)

#crud
@app.route('/crud')
def crud():
    return render_template("crud.html")

#edit sama hapus 
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # Placeholder for database connection setup
    global mydb
    if mydb is None:
        mydb = initialize_database()

    cursor = mydb.cursor(dictionary=True)
    cursor.execute('SELECT * FROM user_data WHERE id = %s', (user_id,))
    user = cursor.fetchone()

    if request.method == 'POST':
        new_email = request.form['email']
        new_password = request.form['password']

        # Update the user's email and password
        cursor.execute('UPDATE user_data SET email = %s, password = %s WHERE id = %s', (new_email, new_password, user_id))
        mydb.commit()

        return redirect('/crud')  # Redirect to the CRUD page after editing

    return render_template('edit.html', user=user)


@app.route('/delete/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute('DELETE FROM user_data WHERE id = %s', (user_id,))
    mydb.commit()

    return redirect('/crud')  # You can redirect to a different page after deleting


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/about_us')
def about():
    return render_template("AboutUs.html")

#pembayaran link
@app.route('/tks')
def tks():
    return render_template('tks.html')

@app.route('/gagal')
def ggl():
    return render_template('gagal.html')

@app.route('/error')
def err():
    return render_template('error.html')


if __name__== '__main__':
    app.run(debug=True)
