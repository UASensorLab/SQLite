from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        new_user = User(username=username, password=hashed_password)

        with app.app_context():
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
            except IntegrityError:
                db.session.rollback()
                return render_template('register.html', error="Username already exists")

    return render_template('register.html', error=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        with app.app_context():
            user = User.query.filter_by(username=username, password=hashed_password).first()

        if user:
            return f'Login successful, welcome {username}!'
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html', error=None)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)



