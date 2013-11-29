from app import app, l
import re
from flask import render_template,request
from flask.views import MethodView
from apperror import *
from flask import jsonify
import json
app.config['SECRET_KEY'] = 'don`t tell anybody,sdfsdfsdfzssdfsdfewwefwe'
from models import User



def query_email(email):
    return l.session.query(User).filter_by(email =email).all()
    

def need_auth(role):
	def _need_auth(func):
		def __need_auth(*args,**kw):
			try:
				sid = request.args['token']
			except:
				raise NoTokenException()
			
			#User.get(sid)
			return func(*args,**kw)
		return __need_auth
	return _need_auth

vemail = re.compile('\w+\@\w\.\w+')

		
@app.route('/')
@need_auth('admin')
def hello():
	return 'hello,world'
	
def jmsg(code):
    code = int(code)
    emsgs = ('lack of email address', 
   'email address duplicated',  )
    msgs = ('email usable', )
    if code > 0:
        msg = msgs[code-1]
    else:
        msg = emsgs[-code -1]
        
    return jsonify({'status': int(code),'msg':msg})
    
class RegisterAPI(MethodView):

        def get(self):
                email = request.args.get('email',None)
                if email == None:
                    return jmsg(-1)
                if vemail.match(email):
                    if query_email():
                        return jmsg(-2)
                
                return jmsg(1)
        
        def post(self):
            r = json.loads(request.data)
            
            
            return 'hi, %s' % r['username']
            

register_view = RegisterAPI.as_view('register')
app.add_url_rule('/capi/register', view_func = register_view  )



	
