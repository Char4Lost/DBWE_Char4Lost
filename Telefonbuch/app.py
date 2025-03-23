from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy # SQL DB
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user # Login
from werkzeug.security import generate_password_hash, check_password_hash  # Passwort-Hashing

import pymysql
pymysql.install_as_MySQLdb()


# Flask-App initialisieren
app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://char4lost:Gh76-Z73-tgIU7!@char4lost.mysql.pythonanywhere-services.com/char4lost$default'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Benutzer-Datenbankmodell
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Personen-Datenbankmodell
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    telefonnummer = db.Column(db.String(20), nullable=False)

# Merkt sich angemeldete User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Startseite mit Suchfunktion (index.html)
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    personen = []
    if request.method == 'POST':
        suchname = request.form.get('name')
        personen = Person.query.filter(Person.name.contains(suchname)).all()
    return render_template('index.html', personen=personen)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Bitte fülle alle Felder aus.', 'error')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Erfolgreich eingeloggt!', 'success')
            return redirect(url_for('index'))
        flash('Benutzername oder Passwort ungültig', 'error')

    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    session.pop('_flashes', None)  # Alte Flash-Nachrichten löschen
    logout_user()
    flash("Du hast dich erfolgreich abgemeldet.")
    return redirect(url_for('login'))

# Registrierung
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('Bitte fülle alle Felder aus.', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Benutzername bereits vergeben', 'error')
            return redirect(url_for('register'))
            
        if User.query.filter_by(email=email).first():
            flash('E-Mail bereits registriert', 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrierung erfolgreich! Bitte melde dich an.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# WIRD NICHT MEHR BENÖTIGT - WAR FÜR DIE ERSTEN DATEN
# Datenbank füllen
#@app.cli.command('seed')
#def seed_db():
#    beispieldaten = [
#        Person(name='Max Mustermann', adresse='Musterstrasse 1, 6001 Luzern', telefonnummer='044 815 01 02'),
#        Person(name='Jack Shepard', adresse='Inselstrasse 4, 8000 Zürich', telefonnummer='044 865 32 54'),
#        Person(name='Jack Shepard', adresse='Obere Gasse 9, 8155 Niederhasli', telefonnummer='043 865 23 99')
#    ]
#    db.session.bulk_save_objects(beispieldaten)
#    db.session.commit()
#    print("Beispieldaten wurden eingefügt!")

# App starten
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)