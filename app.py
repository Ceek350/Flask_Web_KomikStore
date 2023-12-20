from flask import Flask, render_template, url_for



app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
@app.route('/home')
def index():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")

@app.route('/about_us')
def about():
    return render_template("AboutUs.html")

if __name__== '__main__':
    app.run(debug=True)