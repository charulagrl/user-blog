from models import Post, User, Like
from google.appengine.ext import ndb
from main import BlogHandler

class LikeHandler(BlogHandler):
	"""
		Handler to like a blog post
	"""
	def get(self, post_id):

		user_id = self.read_secure_cookie('user')

		# Logged out user will be taken to login page 
		if not user_id:
			self.redirect('/login')

		else:

			user_key = ndb.Key('User', int(user_id))		
			post_key = ndb.Key('Post', int(post_id))

			# Allow like if user is logged in and has not liked the post already.
			# Do not allow author to like his own post
			like = Like.create_like(post_key, user_key)

			self.redirect('/post/%s' %(post_id))

