from mongoengine import *
from flask import Flask, render_template
import json
from collections import namedtuple
from pymongo import MongoClient
import pandas as pd
import os
import csv
from flask import jsonify

app = Flask(__name__)
app.config.from_object('config')

connect('test')
client = MongoClient()
db = client.test

class Country(Document):
    name = StringField()
    data = DictField()    

@app.route('/')
def country():
    for file in os.listdir(app.config['FILES_FOLDER']):
        filename = os.fsdecode(file)
        path = os.path.join(app.config['FILES_FOLDER'],filename)
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile) 
            d = list(reader)
            for data in d:
                country = Country() # a blank placeholder country
                dict = {} # a blank placeholder data dict
                for key in data: # iterate through the header keys
                    if key == "country":
                        # check if this country already exists in the db
                        country_exists = db.country.find({"name" :data.get(key)}).count() > 0
                        
                        # if the country does not exist, we can use the new blank country we created above, and set the name
                        if not country_exists:
                            country.name = data.get(key)
                        # if the country already exists, replace the blank country with the existing country from the db, 
                        # and replace the blank dict with the current country's data 
                        else:
                            country = Country.objects.get(name = data.get(key))
                            dict = country.data
                    else:
                        f = filename.replace(".csv","") # we want to trim off the ".csv" as we can't save anything with a "." as a mongodb field name
                        if f in dict: # check if this filename is already a field in the dict
                            dict[f][key] = data[key] # if it is, just add a new subfield which is key : data[key] (value)
                        else:
                            dict[f] = {key:data[key]} # if it is not, create a new object and assign it to the dict

                    # add the data dict to the country
                    country.data = dict

                # save the country
                country.save()
    return render_template("base.html", title = "Home", page="home")

@app.route('/countries/<country_name>', methods=['GET'])
def countryd3(country_name=None):
    country_data = None
    if country_name is None:
        country_data = Country.objects
        return country_data.to_json()
    else:
        try:
            country_data = Country.objects.get(name = country_name)
            return country_data.to_json()
        except:
            print("=================exception======================")
            countries = "Country not found"
            return countries

@app.route('/')
def index():
    User(email = "jhonr1@otagopoly.ac.nz", first_name = "ruban", last_name = "dass")

    return render_template("base.html", title = "Home", page="home")

@app.route('/inspiration')
def inspiration():
    return render_template("inspiration.html", title = "Inspirations", page="inspiration")

@app.route("/data")       
def group():
    countries_list = db.country.distinct('name')
    return render_template("data.html", title = "Data", page = "data", countries_data = countries_list)    

# 404 error handler
@app.errorhandler(404) 
def page_not_found_404(e):
  return render_template('404.html', title = "Error", error = e), 404
  
# 500 error handler
@app.errorhandler(500) 
def page_not_found_500(e):
  return render_template('500.html', title = "Error", error = e), 500    

if __name__ =="__main__":
    app.run(debug=True, port=8080)
