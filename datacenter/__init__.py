from flask import Flask, render_template, request, session
from flask import send_file, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            username = request.form['username']
            return render_template('index.html')
        return render_template('index.html')


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            data = User.query.filter_by(
                username=name, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return 'Dont Sign in'
        except:
            return "Dont Sign in"


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    """Register Form"""
    if request.method == 'POST':
        new_user = User(username=request.form['username'], password=request.form['password'],
                        email=request.form['email'])

        db.session.add(new_user)
        db.session.commit()
        return render_template('signin.html')
    return render_template('signup.html')


@app.route("/signout")
def signout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))


@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")


@app.route("/Non-Labelled")
def NonLabelled():
    return render_template("NonLabelled.html")


@app.route("/NLupload")
def NLupload():
    return render_template("NLupload.html")


@app.route('/NLsuccess', methods=['GET', 'POST'])
def NLupload_file():
    if request.method == 'POST':
        file = request.files['attach']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("success.html")


@app.route("/Labelled")
def Labelled():
    return render_template("Labelled.html")


@app.route("/Lupload")
def Lupload():
    return render_template("Lupload.html")


@app.route('/Lsuccess', methods=['GET', 'POST'])
def Lupload_file():
    if request.method == 'POST':
        file = request.files['attach']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("success.html")


@app.route("/Verified")
def Verified():
    return render_template("Verified.html")


@app.route("/Vupload")
def Vupload():
    return render_template("Vupload.html")


@app.route('/Vsuccess', methods=['GET', 'POST'])
def Vupload_file():
    if request.method == 'POST':
        file = request.files['attach']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("success.html")


@app.route("/download")
def download():
    download_file = request.args.get('filename')

    return send_from_directory(app.config['UPLOAD_FOLDER'], download_file)
