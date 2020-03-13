from mongoengine import *
from flask import Flask, render_template
import json
from collections import namedtuple
from pymongo import MongoClient
import pandas as pd
import os

app = Flask(__name__)

connect('test')
client = MongoClient()
db = client.test

class User(Document):
    email = StringField()
    first_name = StringField()
    last_name = StringField()

class Country(Document):
    name = StringField()
    population = IntField()

@app.route('/country')
def country():
   countries = [{"name" : "New Zealand", "population" : 450000}]

    # country = db.country
   df = pd.read_csv(os.path.join(os.path.dirname(__file__), "data/country.csv")) #csv file which you want to import
   records = df.to_dict(orient = 'records')
   result = db.country.insert_many(records)

    # for country in countries:
    #     Country(**country).save()
    
   return Country.objects.to_json()

@app.route('/')
def index():
    User(email = "jhonr1@otagopoly.ac.nz", first_name = "ruban", last_name = "dass")

    return render_template("base.html", message = "Home", page="home")

@app.route('/inspiration')
def inspiration():
    return render_template("inspiration.html", title = "Inspirations", page="inspiration")

@app.route("/loadData")       
def loadData():
    return render_template("data.html", title = "Data", page="loadData")

@app.route("/layout")       
def layout():
    return render_template("layout.html", title = "Data")    

@app.route("/sample")       
def sample():
    return render_template("sample.html", title = "sample")

@app.route('/listUsersTest')
def listUsersTest():
    return User.objects.to_json()

if __name__ =="__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
