from mongoengine import *
from app import db
from app.authorize import make_secure_token
import datetime

class User(db.Document):
	config_collection_name = 'users'
	name = StringField()
	password = StringField()
	sex = BooleanField()
	weibo_uid = IntField()
	weibos = ListField(ReferenceField('Weibo'))
	age = IntField(min_value=0, required = False)
	email = EmailField()
	bio = StringField(max_length=1000, required= False)
	sign = StringField(max_length=100,required = False)
	
	weibo_auth_id = IntField(required = False)
	face = StringField(max_length = 255)
	blogcount = IntField(required = False)
	fanscount = IntField(required = False)
	uptime = DateTimeField(required =False)
	fans = ListField(EmbeddedDocumentField('UserFans'))
	created_at = DateTimeField()
	sid = StringField(required = False)
	sid_expires = DateTimeField(required = False)
	meta = {
		'index_options':{'email':1,'sid':1}
		}
	def _gen_sid(self):
		o = str(datetime.datetime.now())
		return make_secure_token(o)
	
	def make_sid(self,expires = datetime.timedelta(days = 10)):
		self.sid = self._gen_sid()
		self.sid_expires = expires+datetime.datetime.now()
	
	
	
class Notice(db.Document):
	user = ReferenceField(User)
	message = StringField(max_length=1000)
	status = BooleanField();
	uptime = DateTimeField()

class UserFans(db.EmbeddedDocument):
	follower = ReferenceField(User)
	uptime = DateTimeField()
	
class WeiboAuth(db.Document):
	access_token = StringField()
	expires_in = DateTimeField()
	weibo_id = IntField()

class Comment(db.EmbeddedDocument):
	content = StringField(max_length= 1000)
	uptime = DateTimeField()
	
class Weibo(db.Document):
	content = StringField()
	comments =  ListField(EmbeddedDocumentField(Comment))

	
if __name__ == '__main__':
	pass
