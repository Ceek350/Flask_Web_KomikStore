from flask import Flask, render_template, url_for, request, redirect, session, jsonify, send_file
import os
import mysql.connector
import re
import subprocess as sp
import base64
import zlib
import hashlib 
from hashlib import sha256
from passlib.hash import sha256_crypt
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


CLIENT_KEY = 'SB-Mid-client-Ay1WobiGTcJNoVKs'



app = Flask(__name__, template_folder='templates', static_folder='static')

UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

app.secret_key = 'komikstore'
allowed_api_keys = ['abc123', '123abc']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def check_api_key(apiKey):
    return apiKey in allowed_api_keys


def initialize_database():
    # Placeholder for your actual MySQL database connection setup
    mydb = mysql.connector.connect(
    host='sql.freedb.tech',
    user='freedb_zerostore',
    port=3306,
    password='9XcMJypct#5tX&J',
    database='freedb_zerostore')
    return mydb

mydb = initialize_database()

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5000'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    return response

@app.route('/')
def anu():
    return render_template('index.html', user=None)

@app.route('/product_page')
def ind_anu():
    return render_template('index2.html', user=None)

#admin page
@app.route('/admin_page')
def admin():
    user = None
    if 'email' in session and session['email'] == admin_email:
        # Assuming you want to display the admin's information
        user = {'email': admin_email, 'password': admin_password}

        return render_template('admin_page.html', user=user)
    else:
        return redirect('/login_admin')

@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/invoice')
def invoice():
    return render_template('invoice.html')

@app.route('/edit_page')
def edit_page():
    return render_template('edit_page.html')

#admin page

@app.route('/logo', methods=['POST'])
def logo_1():
    if 'image' not in request.files:
        return redirect(request.url)

    image = request.files['image']

    if image.filename == '':
        return redirect(request.url)

    if image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'logo_1.png')
        image.save(filename)
        # Lakukan sesuatu dengan gambar yang diunggah (misalnya, menampilkan di halaman atau menyimpan nama file di database)
        return render_template('edit_page')

@app.route('/logoo', methods=['POST'])
def logo_2():
    if 'image' not in request.files:
        return redirect(request.url)

    image = request.files['image']

    if image.filename == '':
        return redirect(request.url)

    if image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'logo_2.png')
        image.save(filename)
        # Lakukan sesuatu dengan gambar yang diunggah (misalnya, menampilkan di halaman atau menyimpan nama file di database)
        return render_template('edit_page')
    
@app.route('/banner_a', methods=['POST'])
def upload_banner_a():
    if 'image' not in request.files:
        return redirect(request.url)

    image = request.files['image']

    if image.filename == '':
        return redirect(request.url)

    if image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'banner_a.png')
        image.save(filename)
        # Lakukan sesuatu dengan gambar yang diunggah (misalnya, menampilkan di halaman atau menyimpan nama file di database)
        return render_template('edit_page')

@app.route('/banner_b', methods=['POST'])
def upload_banner_b():
    if 'image' not in request.files:
        return redirect(request.url)

    image = request.files['image']

    if image.filename == '':
        return redirect(request.url)

    if image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'banner_b.png')
        image.save(filename)
        # Lakukan sesuatu dengan gambar yang diunggah (misalnya, menampilkan di halaman atau menyimpan nama file di database)
        return render_template('edit_page')
    
@app.route('/banner_c', methods=['POST'])
def upload_banner_c():
    if 'image' not in request.files:
        return redirect(request.url)

    image = request.files['image']

    if image.filename == '':
        return redirect(request.url)

    if image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'banner_c.png')
        image.save(filename)
        # Lakukan sesuatu dengan gambar yang diunggah (misalnya, menampilkan di halaman atau menyimpan nama file di database)
        return render_template('edit_page')

@app.route('/admin_login')
def login_admin():
    return render_template('login_admin.html')

admin_email = 'admin@gmail.com'
admin_password = 'admin123'

@app.route('/login_admin', methods=['GET', 'POST'])
def loginAdmin():
    # Output message if something goes wrong...
    msg = ''

    # Check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']

        # Check if the provided email and password match the hardcoded admin credentials
        if email == admin_email and password == admin_password:
            session['email'] = email
            return redirect('/admin_page')  # Redirect to the home page after successful login
        else:
            msg = 'Invalid email or password'

    # Show login form with message (if any)
    return render_template('login_admin.html', msg=msg)

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
    
@app.route('/me')
def me():
    return render_template('portofolio.html')

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

@app.route('/logout_admin')
def logout_admin():
    session.pop('email', None)
    return redirect('/login_admin')

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

@app.route('/tambahdb', methods=['GET', 'POST'])
def tambah_product():
    msg = ''

    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        desc = request.form['desc']

        if 'image' not in request.files:
            msg = 'No file part in the request.'
        else:
            image = request.files['image']

            if image.filename == '':
                msg = 'No selected file.'
            elif image and allowed_file(image.filename):
                # Secure the filename to prevent malicious file names
                filename = secure_filename(image.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Save the file on the server
                image.save(filepath)

                cursor = mydb.cursor(dictionary=True)
                cursor.execute('INSERT INTO db_product (id, title, image, price, description) VALUES (NULL, %s, %s, %s, %s)',
                               (title, filename, price, desc,))
                mydb.commit()
                msg = 'Berhasil Menambahkan'
            else:
                msg = 'File type not allowed. Please upload a valid image.'

    return render_template('tambah.html', msg=msg)


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

@app.route('/api/product', methods=['GET'], endpoint='/api/product')
def get_product():
    print ('Request received for /api/product')
    apiKey = 'abc123'
    if not apiKey or not check_api_key(apiKey):
        return jsonify({'message': 'Unauthorized'}, 401)

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM db_product where id")
    columns = [column[0] for column in cursor.description]
    products = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()

    return jsonify(data=products)

#crud
@app.route('/crud')
def crud():
    return render_template("crud.html")

@app.route('/product')
def product_load():
    return render_template("product.html")

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

@app.route('/editdb/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    # Placeholder for database connection setup
    global mydb
    if mydb is None:
        mydb = initialize_database()

    cursor = mydb.cursor(dictionary=True)
    cursor.execute('SELECT * FROM db_product WHERE id = %s', (product_id,))
    product = cursor.fetchone()

    msg = ''

    if request.method == 'POST':
        new_title = request.form['title']
        new_price = request.form['price']
        new_desc = request.form['desc']

        if 'image' not in request.files:
            msg = 'No file part in the request.'
        else:
            image = request.files['image']

            if image.filename == '':
                msg = 'No selected file.'
            elif image and allowed_file(image.filename):
                # Secure the filename to prevent malicious file names
                filename = secure_filename(image.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # Save the file on the server
                image.save(filepath)

                # Update the database with the new information, including the file path
                cursor.execute('UPDATE db_product SET title = %s, image = %s, price = %s, description = %s WHERE id = %s',
                               (new_title, filename, new_price, new_desc, product_id))
                mydb.commit()
                msg = 'Berhasil Menambahkan'
            else:
                msg = 'File type not allowed. Please upload a valid image.'

        return redirect('/admin_page')  # Redirect to the CRUD page after editing

    return render_template('edit_product.html', product=product, msg=msg)


@app.route('/delete/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute('DELETE FROM user_data WHERE id = %s', (user_id,))
    mydb.commit()

    return redirect('/crud')

@app.route('/deletedb/<int:product_id>', methods=['GET'])
def delete_product(product_id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute('DELETE FROM db_product WHERE id = %s', (product_id,))
    mydb.commit()

    return redirect('/admin_page')


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/tambah')
def tmbh():
    return render_template("tambah.html")

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

#API Free
@app.route('/test')
def test():
    data = {"siapa aku?":"aku seorang web developer"}
    return jsonify(data)


if __name__== '__main__':
    app.run(debug=True)
