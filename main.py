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


from flask import Flask , request,jsonify, redirect,render_template
from APIs import Google_Places_Api, config
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm, CsrfProtect
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
import pymongo
app = Flask(__name__)



csrf = CsrfProtect()

csrf.init_app(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'testWinWin',
    'host': config.DB_URL
}

db = MongoEngine(app)
app.config['SECRET_KEY'] = '_no_one_cared_til_i_put_on_the_mask_'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Document):
    meta = {'collection': 'accounts'}
    username = db.StringField()
    name = db.StringField()
    email = db.StringField(max_length=30)
    password = db.StringField()

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

class RegForm(FlaskForm):
    username = StringField('username',  validators=[InputRequired(), Length(max=30)])
    name = StringField('name',  validators=[InputRequired(), Length(max=30)])
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=0, max=20)])

class LogInForm(FlaskForm):
    username = StringField('username',  validators=[InputRequired(), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])


#***CODE FOR ROUTING***

#Every route is declared with an app.route call

@app.route("/testLogin", methods=['GET', 'POST'])
def home():
    form = LogInForm()
    if request.method == 'GET':
        if current_user.is_authenticated == True:
            return render_template('place_request.html',user=current_user)
        return render_template('testLogin.html', form=form)
    else:
        check_user = User.objects(username=form.username.data).first()
        if check_user:
            if check_password_hash(check_user['password'], form.password.data):
                login_user(check_user)
                return render_template('place_request.html', user=current_user)
            return render_template('testLogin.html', form=form, error="Incorrect password!")
        return render_template('testLogin.html', form=form, error="Username doesn't exist!")

@app.route("/testSignup", methods=['GET', 'POST'])
def signup():
    form = RegForm()
    if request.method == 'GET':
        return render_template('testSignup.html', form=form)
    else:
        if form.validate_on_submit():
            existing_email = User.objects(email=form.email.data).first()
            existing_user = User.objects(username=form.username.data).first()
            if existing_email is not None:
                return render_template('testSignup.html', form=form, error="Email taken")  # We should return a pop up error msg as well account taken
            elif existing_user is not None:
                return render_template('testSignup.html', form=form, error="Username taken")
            else:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                newUser = User(username=form.username.data, name=form.name.data, email=form.email.data,
                               password=hashpass).save()
                login_user(newUser)
                return render_template('place_request.html')
        return render_template('testSignup.html', form=form) #We should return a pop up error msg as well bad input

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
    #Example of insert
    toInsert = {"hit": "requestArea"}
    #response = mycol.insert_one(toInsert)
    #print(response)
    #end example
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

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    form = RegForm()
    return render_template('place_request.html', form=form)
