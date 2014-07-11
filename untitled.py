from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True)
	active = db.Column(db.Boolean())

	def __init__(self, username, active=True):
		self.username = username
		self.active = active

	def deactivate(self):
		self.active = False

	@classmethod
	def compute_grocery_stuff(cls):
		pass


u = User()
u.username = 'jesse'

# Insert to the database
db.session.add(u)
db.session.commit()

# Updates instance u's username to 'new name'
u.username = 'new name'
u.active = False
db.session.commit()

u = User.query.filter_by(username='new name').first()
db.session.delete(u)
db.session.commit

# Delete's u
db.session.delete(u)

# Query many matching a specific criteria
users = User.query.filter_by(username='new name', active=True).all()  # [ARRAY]
for u in users:
	u.deactivate()
db.session.commit()

User.query.filter_by(active=True).count() # 3

# Query one mathcing a specific criteria
user = User.query.filter_by(username='new name').first()  # User()


User.query.filter_by(username='blahblah').first()  # None


for name in ['apple', 'a', 'b']:
	u = User()
	u.username = name
	db.session.add(u)
db.session.commit()


# Don
db.create_all()

<div id="content1">
<table class="content" cellpadding="20" cellspacing ="0" width="90%"> 
<tr align="left" height = "240" width = "100">
<td height = "100">
<font color ="black"><strong>DITO YUNG TITLE!</strong><br><br>argbvadsfrgbvsrbsdbzsdfbdszfbdfb</font>
</td>
</tr>
</div>
</table>
<br>