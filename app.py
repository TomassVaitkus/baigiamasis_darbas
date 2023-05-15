from flask import Flask, render_template, request, redirect, url_for, flash
from form import OrderForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bet kokia simbolių eilutė'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    vardas = db.Column(db.String(50))
    pavarde = db.Column(db.String(50))
    address1 = db.Column(db.String(50))
    address2 = db.Column(db.String(50))
    city = db.Column(db.String(50))
    zip_code = db.Column(db.String(50)) 
    telnr = db.Column(db.String(50))
    pastabos = db.Column(db.String(50))


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/register_success')
    return render_template('register.html')

@app.route('/register_success')
def success():
    users = User.query.all()
    return render_template('register_succes.html', users=users)


@app.route('/fill_order', methods=['GET', 'POST'])
def fill_order():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(email=form.email.data,
                      vardas=form.vardas.data,
                      pavarde=form.pavarde.data,
                      address1=form.address1.data,
                      address2=form.address2.data,
                      city=form.city.data,
                      zip_code=form.zip_code.data,
                      telnr=form.telnr.data,
                      pastabos=form.pastabos.data)
        # db.create_all()
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('order_list'))
    return render_template('form.html', form=form)



@app.route('/order_list')
def order_list():
    orders = Order.query.all()
    return render_template('order_list.html', orders=orders)


# @app.route('/form', methods=['GET', 'POST'])
# def form():
#     form = OrderForm()
#     if form.validate_on_submit():
#         return render_template('success.html', form=form)
#     return render_template('form.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username != 'admin' or password != 'admin':
            error = 'Invalid credentials. Please try again.'
        else:
            return redirect(url_for('fill_order'))
    return render_template('login.html', error=error)
  


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)