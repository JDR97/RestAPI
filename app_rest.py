from enum import unique
from urllib import request
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(90), unique = True, nullable = False)
    desp = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.desp}"

@app.route('/')
def index():
    return 'Hello!'

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output = []
    for drink in drinks:
        drink_data = {'name' : drink.name, 'description' : drink.desp}
        output.append(drink_data)

    return {"drinks" : output}
    #return {"Drinks" : "Drink Data"}

@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    #call with jsonify when not working with a dictionary
    return {'name' : drink.name, 'description' : drink.desp}

@app.route('/drinks', methods = ['POST'])
def add_drink():
    drink = Drink(name = request.json['name'], desp = request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id' : drink.id}

@app.route('/drinks/<id>', methods = ['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"Error" : "No Such Item to Delete"}
    db.session.delete(drink)
    db.session.commit()
    return {"Message" : "Successfully Deleted the Item"}

