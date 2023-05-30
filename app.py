from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_migrate import Migrate
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///L:/baigiamasis_darbas/database_file.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  
db = SQLAlchemy(app)
login_manager = LoginManager(app)
Migrate(app, db) 

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    message = db.Column(db.Text)

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, username, password, email):
        self.username = username
        self.password = password 
        self.email = email

    def __repr__(self):
        return f'{self.name} - {self.email} - {self.password}'
    


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Paemimo = db.Column(db.String(100))
    Pristatymo = db.Column(db.String(100))
    Svoris = db.Column(db.String(100))
    Tel_nr = db.Column(db.String(100))
    user_id = db.Column(db.String(100))
    delivered = db.Column(db.Boolean, default=False)

    def __init__(self, Paemimo, Pristatymo, Svoris,Tel_nr,user_id,delivered):
        self.Paemimo = Paemimo
        self.Pristatymo = Pristatymo 
        self.Svoris = Svoris
        self.Tel_nr = Tel_nr
        self.user_id = user_id
        self.delivered = delivered

class SelectedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Paemimo = db.Column(db.String(100))
    Pristatymo = db.Column(db.String(100))
    Svoris = db.Column(db.String(100))
    Tel_nr = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    delivered = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref='selected_data')

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    new_message = Message(name=name, email=email, message=message)
    db.session.add(new_message)
    db.session.commit()
    time.sleep(3)
    flash('Žinutė išsiūsta sėkmingai!')
    return  redirect('/')

@app.route('/')
def home():
    return render_template('home.html')




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



                                                           # cia reikia pakisti sugeneruota df

@app.route('/selected_table_view')
@login_required
def selected_table_view():
    user = current_user
    data = SelectedData.query.filter_by(user_id=user.id).all()

    return render_template('selected_table.html', data=data)


@app.route('/table_view')
@login_required
def table_view():
    # Fetch data from the database
    data = Data.query.all()

    return render_template('table.html', data=data)

@app.route('/selected', methods=['GET', 'POST'])
@login_required
def selected():
    # Fetch data from the database
    user = current_user
    selected_delivered_ids = request.form.getlist('selected')
    selected_delivered_rows = SelectedData.query.filter(SelectedData.id.in_(selected_delivered_ids)).all()

    if selected_delivered_rows:
        for row in selected_delivered_rows:
            row.delivered = True
            data_row = Data.query.get(row.id)
            data_row.delivered = True

        db.session.commit()

    # Fetch updated data from the database
    data = SelectedData.query.filter_by(user_id=user.id).all()

    return render_template('selected_table.html', data=data)


@app.route('/update', methods=['POST'])
def update():
    selected_ids = request.form.getlist('selected')
    selected_rows = Data.query.filter(Data.id.in_(selected_ids)).all()

    user = current_user
    for row in selected_rows:
        new_row = SelectedData(Paemimo=row.Paemimo, 
                               Pristatymo=row.Pristatymo, 
                               Svoris=row.Svoris,
                               Tel_nr=row.Tel_nr,
                               user_id=user.id, 
                               delivered=row.delivered)
        db.session.add(new_row)

    db.session.commit()
    return redirect(url_for('table_view'))



@app.route('/confirm_delivery', methods=['POST'])
@login_required
def confirm_delivery():
    selected_ids = request.form.getlist('selected')
    selected_rows = SelectedData.query.filter(SelectedData.id.in_(selected_ids)).all()

    for row in selected_rows:
        row.delivered = True
        data_row = Data.query.get(row.id)
        data_row.delivered = True

    db.session.commit()

    return redirect(url_for('selected_table_view'))



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/login_succes')
def login_succes():
    return render_template('login_succes.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('login_succes'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            # flash('Username already exists. Please choose a different username.')
            return redirect(url_for('register'))

        # Create a new user object
        new_user = User(username=username, password=password, email=email)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')



if __name__ == '__main__':
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created.")
    app.run(debug=True)