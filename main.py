'''
SET UP INFO:
1. Install Python 3
2. CD into the CS411 directory on your machine via the command line
3. Run 'pip3 install Flask'
4. Run 'pip3 install pymongo'
5. Run 'export FLASK_APP=main.py' or For windows: $env:FLASK_APP = "main.py" , or set FLASK_APP=main.py
6. Run 'python3 -m flask run'
7. Go to http://127.0.0.1:5000/ (or http://localhost:5000/) in your browser
8. Do ‘CTRL+C’ in your terminal to kill the instance.
9. To auto update the instance once you save ,export FLASK_DEBUG=1 or windows:  $env:FLASK_DEBUG = "main.py"
'''


from flask import Flask , request,jsonify, redirect
from flask import render_template
from APIs import Google_Places_Api
from APIs import config
import json
import pymongo
app = Flask(__name__)

#***CODE FOR MONGO***

#We'll move DB_URL to a secret file once we set it up so we don't push sensitive info to github.
#DB_URL = "MONGO URL HERE"

#Connects program to Mongo instance
#myclient = pymongo.MongoClient(DB_URL)

#The string in brackets represents the database we want to access. If it doesn't exist, it'll make one.
#mydb = myclient["test_database"]

#The string in brackets represents the collection we want to access. If it doesn't exist, it'll make one.
#mycol = mydb["test_collection"]

#inset, query, find, and code for other interactions can be found here: https://www.w3schools.com/python/python_mongodb_insert.asp

#***CODE FOR ROUTING***

#Every route is declared with an app.route call
@app.route("/")
def landing_page():
    data = "Hello World, SUP"
    #render_template looks for a matching file in templates folder to render, and passes the data along that a user specifys
    #Flask by default uses Jinga2 templating. It's essientially html with if statements. You can find more info here: http://jinja.pocoo.org/docs/2.10/
    return render_template('landing_page.html', example_data=data)

#An example of a route that changes based on the input of the endpoint. Notice how '<name>' is a variable.
#http://127.0.0.1:5000/example/mike will return a UI different than http://127.0.0.1:5000/example/tessa, for instance.
@app.route("/example/")
@app.route("/example/<name>")
def example(name=None):
    if name:
        length = len(name)
    else:
        length = 0
    return render_template('example.html', name=name, length=length)


#Go to THIS URL To insert the area you want to go to
@app.route("/requestarea/")
def requestare():
    return render_template('place_request.html')


#This once gets routed to from the above one, DONT ACCESS THIS DIRECTLY
@app.route("/places/", methods = ['GET','POST'])
def place():
    data = "NO DATA"
    if request.method == 'POST':
        place = request.form['location']
        data= Google_Places_Api.get_restaurants_near_place(place,'Restaurants')
        data=data["results"]
        names = []
        address = []
        pics = []
        for d in data:
            names.append(d["name"])
            address.append(d["formatted_address"])
            temp = d["photos"][0]["photo_reference"]
            temp = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=" + temp + "&key=" + config.api_key_google_places
            pics.append(temp)
        response = json.dumps(data, sort_keys = True, indent = 4, separators = (',', ': '))
        return render_template('places.html', place=place, data=response, names = names, address = address, pics = pics)
    else:
        return redirect("/requestarea/")
