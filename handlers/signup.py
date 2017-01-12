from models import Post, User
from google.appengine.ext import ndb
from main import BlogHandler
from utils import make_secure_val

def valid_username(username):
	"""
		Checks if username is valid by matching regex
	"""
	USER_RE = re.compile(r"^[a-zA-z0-9_-]{3,20}$")
	return username and USER_RE.match(username)

def valid_password(password):
	""" 
		Checks if password is valid by matching regex
	"""
	PASSWORD_RE = re.compile(r"^[a-zA-z0-9@#$]{4,20}$")
	return password and PASSWORD_RE.match(password)

def valid_email(email):
	"""
		Checks if email is valid by matching regaex
	"""
	EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
	return email and EMAIL_RE.match(email)

def check_unique_username(username):
	"""
		Check if the username is unique
	"""
	user = User.query(User.username == username).get()
	if not user:
		return True
	else:
		return False

class SignupHandler(BlogHandler):
	"""
		Handler to allow user to create a account
	"""
	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		verify_password = self.request.get('verify')
		email = self.request.get('email')
		params = dict(username=username, email=email)
		is_error = False

		# Check for each validation and add errors to params
		if not valid_username(username):
			params['error_username'] = "That's not a valid username. Username should be minimum 3 letters and can include {a-z, A-Z, 0-9, _, -}."
			is_error = True
		if not valid_password(password):
			params['error_password'] = "That's not a valid password. Password should be minimum 4 letters and can include {@, $, #, a-z, A-Z, 0-9}."
			is_error = True
		if email and not valid_email(email):
			params['error_email'] = "That's not a valid email."
			is_error = True
		if password != verify_password:
			params['error_verify'] = "Your passwords didn't match."
			is_error = True
		if not check_unique_username(username):
			params['error_unique_username'] = "This username already exists."
			is_error = True

		if is_error:
			# In case of error, reloads the signup page and displays the errors
			self.render('signup.html', **params)
		else:
			# store hashed password
			hashed_password = make_secure_val(password)
			user = User(username=username, password=hashed_password)
			user.put()
			# Set-up cookie
			self.login(user)
			self.redirect('/welcome')	

	def get(self):
		self.render('signup.html')
