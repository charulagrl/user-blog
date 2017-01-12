from models import User
from main import BlogHandler
from utils import make_secure_val

def valid_username(username):
	user = User.query(User.username == username).get()
	if user:
		return True
	else:
		return False

class LoginHandler(BlogHandler):
	""" 
		Handler to allow user login
	"""
	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')

		params = dict(username=username, password=password)

		# Check if the username is valid
		if not valid_username(username):
			params['error_username'] = "This username does not exist."
			self.render("login.html", **params)
		else:
			hashed_password = make_secure_val(password)
			# Check if user exist for a username and password
			user = User.query(User.username == username, User.password == hashed_password).get()

			if not user:
				params['error_password'] = "This is an invalid password"
				self.render("login.html", **params)
			else:
				self.login(user)
				self.redirect("/welcome")

	def get(self):
		self.render('login.html')
