
class WeiboError(Exception):
	pass
    
    
class Unauthorized(WeiboError):
	pass
class ArgumentsError(WeiboError):
	pass

class LackArgumentsError(ArgumentsError):
    pass
class NoTokenException(ArgumentsError):
	pass
