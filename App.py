import re
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func




app = Flask(__name__, template_folder='Template')
app.secret_key="Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

#Employee model
class DATA(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    phone=db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

@app.route('/insert', methods = ['POST'])

#creates new instance of Employee class 
def newEmployee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = DATA(name, email, phone)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee inserted successfully")

        return redirect(url_for("index"))

#update employee info
@app.route('/update', methods =['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = DATA.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash("Employee Updated Successfully")
        return(redirect(url_for('index')))

@app.route('/delete/<id>/')
def delete(id):     
    my_data = DATA.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted")
    return(redirect(url_for('index')))



@app.route('/')

def index():
    all_data = DATA.query.all()
    return render_template("index.html", employees = all_data)

if __name__ == "__main__":
    app.run(debug=True)
