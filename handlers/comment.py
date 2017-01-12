from models import Post, User, Like, Comment
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from main import BlogHandler

class CreateCommentHandler(BlogHandler):

	"""
		Handler to create comments on posts
	"""

	def get(self, post_id):

		self.render('comment.html')

	def post(self, post_id):

		user_id = self.read_secure_cookie('user')

		# User need to be logged in to post comments
		if not user_id:
			self.redirect('/login')

		else:

			post_key = ndb.Key('Post', int(post_id))
			post = post_key.get()
			user_key = ndb.Key('User', int(user_id))
			content = self.request.get('content')

			# Comments cannot be left blank
			if not content:
				error = "Comment can't be blank."
				self.redirect('comment.html', error_content=error)
			else:
				comment = Comment(user=user_key, post=post_key, content=content)
				comment.put()

				self.redirect('/post/%s' % post_id)
