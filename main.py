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


from flask import Flask , request,jsonify, redirect,render_template, url_for, session
from APIs import Google_Places_Api, config
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_oauth import OAuth
from urllib.request import urlopen
from urllib import request as URLLib_request
from urllib import error

import json
import pymongo
import pymongo
app = Flask(__name__)

csrf = CSRFProtect()

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

class RequestForm(FlaskForm):
    area = StringField('location',  validators=[InputRequired(), Length(max=100)])


#***CODE FOR ROUTING***


#Code for GOOGLE AUTHENTICATION

oauth = OAuth()
GOOGLE_CLIENT_ID = config.Google_Client_ID
GOOGLE_CLIENT_SECRET = config.Google_Client_Secret
REDIRECT_URI = '/oauth2callback'
SECRET_KEY = 'SOMETHINGRANDOM_IHATEOAUTH'
google = oauth.remote_app('google',
base_url='https://www.google.com/accounts/',
authorize_url='https://accounts.google.com/o/oauth2/auth',
request_token_url=None,
request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
'response_type': 'code'},
access_token_url='https://accounts.google.com/o/oauth2/token',
access_token_method='POST',
access_token_params={'grant_type': 'authorization_code'},
consumer_key=GOOGLE_CLIENT_ID,
consumer_secret=GOOGLE_CLIENT_SECRET)

access_token = [""]

#Every route is declared with an app.route call
@app.route("/")
def landing_page():
    form_Login = LogInForm()
    form_Request = RequestForm()
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('requestare'))
    access_token = access_token[0]
    headers = {'Authorization': 'OAuth '+access_token}
    req = URLLib_request.Request('https://www.googleapis.com/oauth2/v1/userinfo',headers= headers)
    try:
        opener = URLLib_request.build_opener()
        res = opener.open(req)
        print(res)
    except error.URLError as e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('testLogin'))
        print(res.read())
        return res.read()
    print(res.read())
    return redirect(url_for('testLogin'))

    #OLD CODE
    if current_user.is_authenticated == True or session.get('access_token') is not None:
        data = "Hello World, SUP"
        return render_template('place_request.html',form =form_Request)
    else:
        return render_template('testLogin.html', form=form_Login)


@app.route('/Googlelogin')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('requestare'))
 
@google.tokengetter
def get_access_token():
    return session.get('access_token')

@app.route("/testLogin", methods=['GET', 'POST'])
def testLogin():
    form = LogInForm()
    form_Request = RequestForm()
    if request.method == 'GET':
        if current_user.is_authenticated == True:
            return redirect(url_for('requestare'))
        return render_template('testLogin.html', form=form)
    else:
        check_user = User.objects(username=form.username.data).first()
        if check_user:
            if check_password_hash(check_user['password'], form.password.data):
                login_user(check_user)
                return render_template('place_request.html',form =form_Request)
            return render_template('testLogin.html', form=form, error="Incorrect password!",Client_id_url=config.Google_Client_ID)
        return render_template('testLogin.html', form=form, error="Username doesn't exist!",Client_id_url=config.Google_Client_ID)

@app.route("/testSignup", methods=['GET', 'POST'])
def signup():
    form = RegForm()
    form_Request =  RequestForm()
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
                print("LOGGED IN")
                return render_template('place_request.html',form =form_Request)
        return render_template('testSignup.html', form=form) #We should return a pop up error msg as well bad input


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
@app.route("/requestarea/", methods = ['GET','POST'])
def requestare():
    form = RequestForm()
    if current_user.is_authenticated == True or session.get('access_token') is not None:
        #Example of insert
        toInsert = {"hit": "requestArea"}
        #response = mycol.insert_one(toInsert)
        #print(response)
        #end example
        name = None
        try:
            if(current_user.name.count(" ")>=1):
                name = current_user.name.split(" ")[0]
            else:
                name = current_user.name
        except Exception as e:
            name = None

        return render_template('place_request.html', form=form, name=name)
    else:
        return redirect("/testLogin")

#This once gets routed to from the above one, DONT ACCESS THIS DIRECTLY
@app.route("/places/", methods=['GET','POST'])
def place():
    data = "NO DATA"
    if request.method == 'POST':
        print(request.form)
        place = request.form['area']
        # data= Google_Places_Api.get_restaurants_near_place(place,'Restaurants')
        data = Google_Places_Api.get_museums(place)
        data = data["results"]
        names = []
        address = []
        pics = []
        for d in data:
            names.append(d["name"])
            address.append(d["formatted_address"])
            if "photos" in d:
                temp = d["photos"][0]["photo_reference"]
                temp = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=" + temp + "&key=" + config.api_key_google_places
                pics.append(temp)
            else:
                pics.append("https://safekozani.gr/images/coming-soon.png")
        response = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        return render_template('places.html', place=place, data=response, names=names, address=address, pics=pics)
    else:
        return redirect("/requestarea/")

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    try:
        del session['access_token']
    except Exception:
        pass
    return redirect("/testLogin")
