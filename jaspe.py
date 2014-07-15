import flask, flask.views
from flask import render_template
from flask import session, redirect
from jinja2 import environment, FileSystemLoader
from flask.ext.sqlalchemy import SQLAlchemy
import time
from flask.ext import admin
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin import Admin, BaseView, expose
import os
from flask import url_for, request, session, redirect
from flask_oauth import OAuth

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
app.secret_key = '234234rfascasascqweqscasefqwefe2323234dvsv'
ingredients=[]

FACEBOOK_APP_ID = '539244542865228'
FACEBOOK_APP_SECRET = 'efaee0037f9320831895a5e9aa4d1bc6'

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('email, ')}
)

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)


class recipe3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe3Name = db.Column(db.String(64))
    recipe3Desc = db.Column(db.String(140))
    recipe3Auth = db.Column(db.String(64))
    recipe3facebookId = db.Column(db.String(64))
    recipe3Date = db.Column(db.String(64))
    recipe3Use = db.Column(db.Integer)
    

    def __init__(self, recipe3Name, recipe3Desc, recipe3Auth, recipe3facebookId, recipe3Date, recipe3Use):
        self.recipe3Name = recipe3Name
        self.recipe3Desc = recipe3Desc
        self.recipe3Auth = recipe3Auth
        self.recipe3facebookId = recipe3facebookId
        self.recipe3Date = recipe3Date
        self.recipe3Use = recipe3Use
        


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facebookId = db.Column(db.String(64), unique=True)
    userFname = db.Column(db.String(64))
    userLname = db.Column(db.String(64))
    joinDate = db.Column(db.String(64))
    
    def __init__(self, facebookId, userFname, userLname, joinDate):
        self.facebookId = facebookId
        self.userFname = userFname
        self.userLname = userLname
        self.joinDate = joinDate


class ingr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingrName = db.Column(db.String(64), unique=True)
    ingrCat = db.Column(db.String(140))
    ingrUnit = db.Column(db.String(64))

    def __init__(self, ingrName, ingrCat, ingrUnit):
        self.ingrName = ingrName
        self.ingrCat = ingrCat
        self.ingrUnit = ingrUnit


class recipeIng1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipeId = db.Column(db.String(64))
    IngrId = db.Column(db.String(140))
    riQty = db.Column(db.String(64))
    
    def __init__(self, recipeId, IngrId, riQty):
        self.recipeId = recipeId
        self.IngrId = IngrId
        self.riQty = riQty
        
class recipeInstr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipeId = db.Column(db.String(64))
    instr = db.Column(db.String(1500))
   
    def __init__(self, recipeId, instr):
        self.recipeId = recipeId
        self.instr = instr

class favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipeId = db.Column(db.String(64))
    facebookId = db.Column(db.String(64))
   
    def __init__(self, recipeId, facebookId):
        self.recipeId = recipeId
        self.facebookId = facebookId

class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adminUname = db.Column(db.String(64))
    adminPass = db.Column(db.String(64))
    adminLog = db.Column(db.String(64))
   
    def __init__(self, adminUname, adminPass, adminLog):
        self.adminUname = adminUname
        self.adminPass = adminPass
        self.adminLog = adminLog

# Admin ModelView
class recipe3Admin(sqla.ModelView):
    column_display_pk = True
    
    # form_columns = ['nickname', 'description', 'status']
    # # form_overrides = dict(status=SelectField)
    # # form_args = dict(
    # #          status=dict(
    # #             choices=[('Approved', 'Approved'), ('Pending', 'Pending')]
    # #             ))

admin = Admin(app)
admin.add_view(recipe3Admin(recipe3, db.session))
admin.add_view(recipe3Admin(user, db.session))

 
def index ():
    display=recipe3.query.order_by(recipe3.recipe3Date.desc()) 
    del session['addtorecipeIng'][:]
    del session['addtorecipeQty'][:]
    del session['addtorecipeUnt'][:]
    del session['addtorecipeId'][:]
    return display;  
def ntbk ():
    ing = recipe3.query.filter_by(id=session["id"]).first()
    ing.recipe3Use = ing.recipe3Use + 1
    db.session.commit()

def get_id():
    session["id"] = flask.request.form.get("id", "undefined")
    return session["id"]
    
def get_ing():
    ing = recipe3.query.filter_by(id=session["id"]).first()
    return ing;

def check_instruction():
    i = recipeInstr.query.filter_by(recipeId=get_id()).first()
    if i:
        passinstruct = i.instr
    else:
        passinstruct = "No instructions available."
    return passinstruct

def check_if_fav():
    f = favorites.query.filter_by(recipeId=get_id(), facebookId=session['facebookId']).all()
    if f:
        session["faved"] = True
    else:
        session["faved"] = False
    return session["faved"]

def check_if_fav_afte_favdelete():
    f = favorites.query.filter_by(recipeId=session["id"], facebookId=session['facebookId']).all()
    if f:
        session["faved"] = True
    else:
        session["faved"] = False
    return session["faved"]

def show_recipe():
    results = recipe3.query.filter_by(id=get_id()).all()
    return results

def show_recipe_after_favdelete():
    results = recipe3.query.filter_by(id=session["id"]).all()
    return results

def get_ingridients():
    ings = []
    ingArray = recipeIng1.query.filter_by(recipeId=get_id()).all()
    for x in range (0,len(ingArray)):
        ings.append(ingr.query.filter_by(id=ingArray[x].IngrId).first())
    return ings

def get_ingridients_after_favdelete():
    ings = []
    ingArray = recipeIng1.query.filter_by(recipeId=session["id"]).all()
    for x in range (0,len(ingArray)):
        ings.append(ingr.query.filter_by(id=ingArray[x].IngrId).first())
    return ings

def get_ingridient_quantity():
    qty = []    
    ing = recipeIng1.query.filter_by(recipeId=get_id()).all()
    for x in range (0,len(ing)):
        qty.append(recipeIng1.query.filter_by(recipeId=ing[x].recipeId,IngrId=ing[x].IngrId).first())
    return qty

def get_ingridient_quantity_after_favdelete():
    qty = []    
    ing = recipeIng1.query.filter_by(recipeId=session["id"]).all()
    for x in range (0,len(ing)):
        qty.append(recipeIng1.query.filter_by(recipeId=ing[x].recipeId,IngrId=ing[x].IngrId).first())
    return qty

def most_used():
    display=recipe3.query.order_by(recipe3.recipe3Use.desc())
    return display

def authenticate():
    session['uname'] = flask.request.form.get('userName')
    session['pass'] = flask.request.form.get('userPass')
    if user.query.filter_by(userName=session['uname'], userPass=session['pass']).first():
        session["signedin"] = True
        if session['add']:
            return flask.render_template('index.html', username=session['uname'], \
                display=index(), ings=session['add'],signedin=session["signedin"])
        else:
            return flask.render_template('index.html', username=session['uname'], \
                display=index(), signedin=session["signedin"])
        
    else:
        session["signedin"] = False
        return flask.render_template('index.html', display=index(), ings=session['add'], \
            signedin=session["signedin"])


def empty_sessions():
    session["uname"] = ''
    session["add"] = []
    session["j"] = ''
    session["signedin"] = False
    del session['addtorecipeIng'][:]
    del session['addtorecipeQty'][:]
    del session['addtorecipeUnt'][:]
    del session['ntbkqty'][:]
    del session['ntbkunit'][:]
    del session['add'][:]
    del session['ntbkqty'][:]
    del session['ntbkunit'][:]
    del session['addtorecipeId'][:]
    del session['iddel'][:]


def add_ingredients_to_list():
    addThis = recipeIng1.query.filter_by(recipeId=get_ing().id).all()
    for x in range(0,len(addThis)):
        ings1 = ingr.query.filter_by(id=addThis[x].IngrId).first()
        ingsqty = addThis[x].riQty
        if not ings1.ingrName in session['add']:
            session["iddel"].append(ings1.id)
            session['add'].append(ings1.ingrName)
            session['ntbkqty'].append(float(ingsqty)*float(flask.request.form.get("serving")))
            session['ntbkunit'].append(ings1.ingrUnit)
        else:
            count5 = len(session['add'])
            for x in range(0,count5):
                if ings1.ingrName == session['add'][x]:
                    session['ntbkqty'][x] = float(session['ntbkqty'][x]) + \
                    (float(ingsqty)*float(flask.request.form.get("serving")))

def create_recipe_name_desc():
    recipeName = flask.request.form.get('recipeName')
    recipeDesc = flask.request.form.get('recipeDesc')

    u = recipe3(recipeName,recipeDesc,session['uname'],session['facebookId'], \
        time.strftime("%x %H:%M:%S"),0)
    db.session.add(u)
    db.session.commit()

    getID = recipe3.query.filter_by(recipe3facebookId=session['facebookId']).all()
    session["count2"]= len(getID)
    session["passID"]= getID[session["count2"]-1].id

def get_all_favorites():
    a=[] 
    f = favorites.query.filter_by(facebookId=session['facebookId']).all()
    count6 = len(f)
    for x in range(0, count6):
        a.append(recipe3.query.filter_by(id = f[x].recipeId).first())
    return a

def get_qty():
    addthising = flask.request.form.get("id")
    ing1 = ingr.query.filter_by(id=addthising).first()
    session["passingName"]=ing1.ingrName
    session["passingID"]=ing1.id
    session["passingUnit"]=ing1.ingrUnit
    session["passingCat"]=ing1.ingrCat

def add_to_recipe():
    idwithqty=flask.request.form.get("id")
    quantity=flask.request.form.get("quantity")
    ingtoadd=ingr.query.filter_by(id=idwithqty).first()
    
    if not ingtoadd.ingrName in session['addtorecipeIng']:
        session['addtorecipeIng'].append(ingtoadd.ingrName)
        session['addtorecipeQty'].append(quantity)
        session['addtorecipeUnt'].append(ingtoadd.ingrUnit)
        session['addtorecipeId'].append(ingtoadd.id)

def empty_notebook():
    del session['add'][:]
    del session['ntbkqty'][:]
    del session['ntbkunit'][:]
    del session['iddel'][:]

def insert_this_ing():
    for y in range (0,len(session['addtorecipeIng'])):
        q = ingr.query.filter_by(ingrName=session['addtorecipeIng'][y]).first()
        j = recipeIng1(session["passID"],q.id,session['addtorecipeQty'][y])
        db.session.add(j)
        db.session.commit()
    del session['addtorecipeIng'][:]
    del session['addtorecipeQty'][:]
    del session['addtorecipeUnt'][:]
    del session['addtorecipeId'][:]

def add_instructions():
    session["instr"] = flask.request.form.get("instr")
    if session["instr"]:
        instrtoadd = recipeInstr(session["passID"],session["instr"])
        db.session.add(instrtoadd)
        db.session.commit()

def search():
    session['searchstring'] = flask.request.form.get("searchstring")
    j = ingr.query.filter(ingr.ingrName.like('%'+session['searchstring']+'%')).all()
    return j

def delete_this_ing():
    session["deleteIng"] = flask.request.form.get("id")
    delete = ingr.query.filter_by(id=session["deleteIng"]).first()
    session["deletfromarray"] = session['addtorecipeIng'].index(delete.ingrName)
    del session['addtorecipeIng'][session["deletfromarray"]]
    del session['addtorecipeQty'][session["deletfromarray"]]
    del session['addtorecipeUnt'][session["deletfromarray"]]
    del session['addtorecipeId'][session["deletfromarray"]]

def delete_this_fav():
    d = favorites.query.filter_by(recipeId=session["id"], facebookId=session['facebookId']).first()
    db.session.delete(d)
    db.session.commit()

def delete_this_recipe():
    session["idtodelete"] = flask.request.form.get("id")
    de = recipe3.query.filter_by(id=session["idtodelete"]).first()
    db.session.delete(de)
    db.session.commit()
    d1 = recipeIng1.query.filter_by(recipeId=session["idtodelete"]).all()
    count7=len(d1)
    for x in range(0, count7):
        db.session.delete(d1[x])
    db.session.commit()
    d2 = favorites.query.filter_by(recipeId=session["idtodelete"]).all()
    count7=len(d2)
    for x in range(0, count7):
        db.session.delete(d2[x])
    db.session.commit()

    d3 = recipeInstr.query.filter_by(recipeId=session["idtodelete"]).all()
    count7=len(d3)
    for x in range(0, count7):
        db.session.delete(d3[x])
    db.session.commit()
    b = recipe3.query.filter_by(recipe3facebookId=session['facebookId']).all()
    count4=len(b)
    return b

def delete_from_list():
    deleteList = flask.request.form.get("id")
    delete = ingr.query.filter_by(id=deleteList).first()
    deletfromList = session['add'].index(delete.ingrName)
    del session['add'][deletfromList]
    del session['ntbkqty'][deletfromList]
    del session['ntbkunit'][deletfromList]
    del session['iddel'][deletfromList]


@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index_route')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)
    
    session['signedin'] = True
    session['facebook_token'] = (resp['access_token'], '')
    data = facebook.get('/me').data
    if 'id' in data and 'name' in data:
        session['facebookId'] = data['id']
        session['uname'] = data['first_name']
        session['lname'] = data['last_name']

        if not user.query.filter_by(facebookId=session['facebookId']).first():
            registerUser=user(session['facebookId'],session['uname'],session['lname'],time.strftime("%x %H:%M:%S"))  
            db.session.add(registerUser)
            db.session.commit()
    return redirect(next_url)


@app.route('/', methods=['GET', 'POST'])
def index_route():
    if not session:
        session["signedin"] = False
        session["uname"] = ''
        session["add"] = []
        session["ntbkqty"] = []
        session['ntbkunit']= []
        session["iddel"]= []
        session['addtorecipeIng']= []
        session['addtorecipeQty']= []
        session['addtorecipeUnt']= []
        session['addtorecipeId']= []
        session["returnsearchrecipe"] = []
    if flask.request.method == 'GET':
        return flask.render_template('index.html',signedin=session["signedin"],username=session['uname'], display=index(), ings=session['add'], qty=session['ntbkqty'], \
        unit=session['ntbkunit'], id=session["iddel"])

def search_for_recipe():
    session['search'] = flask.request.form.get("search")
    a = recipe3.query.filter(recipe3.recipe3Name.like('%'+session['search']+'%')).all()
    return a
    

@app.route('/showRecipe', methods=['GET', 'POST'])
def add():

    return flask.render_template('recipeDetails.html', username=session['uname'], results=show_recipe(), ing=get_ingridients(), qty=get_ingridient_quantity(), instr=check_instruction(),fav=check_if_fav())


@app.route('/logout')
def logout():
    empty_sessions() 
    pop_login_session()    
    return redirect("/")


@app.route('/addRecipe', methods=['GET', 'POST'])
def add_recipe():
    return flask.render_template('addRecipe.html')


@app.route('/auth', methods=['GET', 'POST'])
def authenticate_user():
    
    authenticate()
    return flask.render_template('index.html', username=session['uname'], \
                display=index(), signedin=session["signedin"],ings=session['add'], qty=session['ntbkqty'], \
                unit=session['ntbkunit'], id=session["iddel"])


@app.route('/addList', methods=['GET', 'POST'])
def add_list():
    ntbk()
    add_ingredients_to_list()
    return flask.render_template('addList.html', ings=session['add'], qty=session['ntbkqty'], \
        unit=session['ntbkunit'], id=session["iddel"])


@app.route('/uploadForm', methods=['GET', 'POST'])
def upload_form():
    empty_notebook()
    return flask.render_template('uploadForm.html',ings = session['add'])


@app.route('/createRecipe', methods=['GET', 'POST'])
def create_recipe():
    create_recipe_name_desc()
    i = ingr.query.all()
    return flask.render_template('addIng.html', allIng=i, test=session["passID"])


@app.route('/getQty', methods=['GET', 'POST'])
def show_qty():
  
    get_qty()
    return flask.render_template('qty.html', name=session["passingName"], \
        id=session["passingID"], unit=session["passingUnit"], cat=session["passingCat"])


@app.route('/addtorecipe', methods=['GET', 'POST'])
def add_this_recipe():
    add_to_recipe()  
    return flask.render_template('ingrtab.html',id=session['addtorecipeId'], \
        ings2=session['addtorecipeIng'], qty2=session['addtorecipeQty'],unt2=session['addtorecipeUnt'])


@app.route('/insertIngs', methods=['GET', 'POST'])
def insert_ings():
    if session['addtorecipeIng']:
        insert_this_ing()
        return flask.render_template('instructions.html')
    else:
        i = ingr.query.all()
        return flask.render_template('addIng.html', allIng=i, test=session["passID"])


@app.route('/addInstr', methods=['GET', 'POST'])
def insert_instr():

    add_instructions()
    return flask.render_template('index.html', display=index(), username=session['uname'], \
        ings = session['add'], signedin=session['signedin'],qty=session['ntbkqty'], \
        unit=session['ntbkunit'])


@app.route('/searchIng', methods=['GET', 'POST'])
def search_ing():
      
    return flask.render_template('returnsearch.html', searchIng=search())


@app.route('/searchRecipe', methods=['GET', 'POST'])
def search_recipe():
    
    return flask.render_template('returnsearchrecipe.html', searchIng=search_for_recipe())


@app.route('/deleteIng', methods=['GET', 'POST'])
def delete_ing():
    delete_this_ing()
    return flask.render_template('ingrtab.html',id=session['addtorecipeId'], \
        ings2=session['addtorecipeIng'], qty2=session['addtorecipeQty'], unt2=session['addtorecipeUnt'])


@app.route('/viewProfile', methods=['GET', 'POST'])
def view_profile():   
    b = recipe3.query.filter_by(recipe3facebookId=session['facebookId']).all()
    count4=len(b)
    for x in range(0,count4):
        session["returnsearchrecipe"].append(b[x].recipe3Name)
    return flask.render_template('returnuserrecipe.html', searchIng=b, username=session['uname'])  


@app.route('/addFav', methods=['GET', 'POST'])
def add_fav():   
    j = favorites(session["id"],session['facebookId'])
    db.session.add(j)
    db.session.commit()

    return flask.render_template('addFav.html', fav=True)


@app.route('/mostUsed', methods=['GET', 'POST'])
def mostUsed():   
    
    return flask.render_template('mostUsed.html', display=most_used())


@app.route('/mostRecent', methods=['GET', 'POST'])
def mostRecent():   
    
    return flask.render_template('mostRecent.html', display=index())


@app.route('/my_favorites', methods=['GET', 'POST'])
def get_favorites():  
    return flask.render_template('myFav.html', display=get_all_favorites())


@app.route('/deleteFav', methods=['GET', 'POST'])
def delete_favorites():  
    delete_this_fav()
    
    return flask.render_template('recipeDetails.html', username=session['uname'], \
        results=show_recipe_after_favdelete(), ing=get_ingridients_after_favdelete(), qty=get_ingridient_quantity_after_favdelete(), instr=session["passinstruct"],fav=check_if_fav_afte_favdelete())


@app.route('/deleteRecipe', methods=['GET', 'POST'])
def delete_recipe():  
    
    
    return flask.render_template('returnuserrecipe.html', searchIng=delete_this_recipe(), username=session['uname']) 


@app.route('/deleteList', methods=['GET', 'POST'])
def delete_list():
    delete_from_list()
    return flask.render_template('addList.html', ings=session['add'], qty=session['ntbkqty'], unit=session['ntbkunit'], id=session["iddel"])


@app.route('/plain', methods=['GET', 'POST'])
def view_plain():

    return flask.render_template('plain.html', ings=session['add'], qty=session['ntbkqty'], unit=session['ntbkunit'], id=session["iddel"])


@app.route('/admin', methods=['GET', 'POST'])
def prompt_to_log():

    return flask.render_template('adminLog.html')


@app.route('/mostRecent', methods=['GET', 'POST'])
def most_recent():

    return flask.render_template('mostRecent.html', display=index())


@app.route('/adminAuth', methods=['GET', 'POST'])
def admin_page():
    session['adminUname'] = flask.request.form.get('adminUname')
    session['adminPass'] = flask.request.form.get('adminPass')
    if admin.query.filter_by(adminUname=session['adminUname'], adminPass=session['adminPass']).first():
        return flask.render_template('adminPage.html', adminUname=session['adminUname'])
    else:
        return flask.render_template('adminLog.html')


@app.route('/db/rebuild')
def db_rebuild():
    db.drop_all()
    db.create_all()
    return os.environ['DATABASE_URL']

if __name__ == '__main__':
    app.debug = True
    app.run(port=int(os.environ['PORT']), host='0.0.0.0')
