
import flask.ext.login as fLogin

class User(fLogin.UserMixin)

	def __init__(self, name, password):
		
		self.name = name
		self.password = password
		
