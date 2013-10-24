from app import app
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired
from flask import render_template,request
from flask.views import MethodView


app.config['SECRET_KEY'] = 'don`t tell anybody,sdfsdfsdfzssdfsdfewwefwe'

class RegisterForm(Form):
	username = TextField('username',validators=[DataRequired()])
	
class WeiboError(Exception):
	pass
class Unauthorized(WeiboError):
	pass
class ArgumentsError(WeiboError):
	pass
class NoSidException(ArgumentsError):
	pass

def need_auth(role):
	def _need_auth(func):
		def __need_auth(*args,**kw):
			try:
				sid = request.args['sid']
			except:
				raise NoSidException()
			
			#User.get(sid)
			return func(*args,**kw)
		return __need_auth
	return _need_auth

		
@app.route('/')
@need_auth('admin')
def hello():
	return 'hello,world'
	
class RegisterAPI(MethodView):

        def get(self):
                email = request.args.get('email',None)
                




	
