import sys
sys.path.insert(0,'../')
from app.models import *
from datetime import datetime
def create_Notice():
	return Notice(userid=12333,message = 'hello,test',
		status = False,uptime = datetime.utcnow())
		
def create_UserFans():
	return  UserFans(userid=12333,fansid=12123213,uptime = datetime.utcnow())

def create_WeiboAuth():
	return  WeiboAuth(access_token="sdfasdfklsafjasklfjs",
		expires_in = datetime.utcnow(),
		weibo_id = 12312312)
		
def create_Comment():
	return  Comment(
		content = 'hello,comment',
		uptime = datetime.utcnow())
	

def create_User():
	c = create_Comment()
	return  User(name = 'bowman han', password = 'md5pass',
		weibo_uid = 123123123, age = 12,
		email = 'fancycode@gmail.com',
		sign = 'http://icon.com/123',
		bio = 'computer science',
		face = 'http://icon.com/hd123',
		created_at  = datetime.utcnow(),
		comments = [c,])
def create_Admin():
	c = create_Comment()
	return  Admin(name = 'bowman han', password = 'md5pass',
		weibo_uid = 123123123, age = 12,
		email = 'fancycode@gmail.com',
		sign = 'http://icon.com/123',
		bio = 'computer science',
		face = 'http://icon.com/hd123',
		created_at  = datetime.utcnow(),
		comments = [c,])

def test_create_models():
	notice = create_Notice();
	userFans = create_UserFans()
	comment = create_Comment()
	weiboAuth = create_WeiboAuth()
	user = create_User()

def test_adding_comment_to_user():
	u = create_User()
	c = create_Comment()
	u.comments.append(c)
	s = Session.connect('test')
	s.insert(u)
	s.flush()

	
	
