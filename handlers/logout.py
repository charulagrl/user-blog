from main import BlogHandler

class LogoutHandler(BlogHandler):
	""" Handler to logout the user
	"""
	def get(self):
		# delete the cookie
		self.logout()

		self.redirect('/login')
