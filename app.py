from flask import Flask, render_template, request, redirect, url_for, flash
from form import OrderForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# db = SQLAlchemy()

# class Order(db.Model):
#     __tablename__ = 'orders'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(50))
#     vardas = db.Column(db.String(50))
#     pavarde = db.Column(db.String(50))
#     address1 = db.Column(db.String(50))
#     address2 = db.Column(db.String(50))
#     city = db.Column(db.String(50))
#     zip_code = db.Column(db.String(50)) 
#     telnr = db.Column(db.String(50))
#     pastabos = db.Column(db.String(50))
    
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bet kokia simbolių eilutė'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
# Migrate(app, db)


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
    
# db.create_all()

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
        db.create_all()
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



@app.route('/', methods=['GET', 'POST'])
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
  app.run(host='127.0.0.1', port=8000, debug=True)