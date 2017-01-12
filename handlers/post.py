from models import Post, User, Comment
from google.appengine.ext import ndb
from main import BlogHandler


class CreatePostHandler(BlogHandler):
	"""
		Handler to create blog post
	"""
	def post(self):

		user_id = self.read_secure_cookie('user')

		# Takes user to the login page if he/she is not signed-in
		if not user_id:
			self.redirect('/login')
	
		else:
			title = self.request.get('subject')
			content = self.request.get('content')		
			author_key = ndb.Key('User', int(user_id))

			is_error = False
			params = dict(title=title, content=content)

			if not title:
				params['error_title'] = "Title cannot be blank"
				is_error = True

			if not content:
				params['error_content'] = "Content can't be blank"
				is_error = True

			if is_error:
				# In case of error, the post form will be re-render again
				self.render('create_post.html', **params)
			else:
				post = Post(title=title, content=content, author=author_key)
				post.put()
				self.redirect('/')
		

	def get(self):
		user_id = self.read_secure_cookie('user')

		# Takes user to the login page if he/she is not signed-in
		if not user_id:
			self.redirect('/login')
		else:
			self.render('create_post.html')


class EditPostHandler(BlogHandler):
	"""
		Handler to edit existing posts
	"""
	def get(self, post_id):

		user_id = self.read_secure_cookie('user')

		# Takes user to the login page if he/she is not signed-in
		if not user_id:
			self.redirect('/login')

		else:
			post_key = ndb.Key('Post', int(post_id))
			post = post_key.get()

			author_key = ndb.Key('User', int(user_id))

			# Only author of the post is allowed to do the editing
			if author_key != post.author:
				error_permission = "You are not allowed to edit this post"
				self.render('post.html', post=post, error_permission=error_permission)
			else:
				self.render('edit_post.html', post=post)

	def post(self, post_id):
		post_key = ndb.Key('Post', int(post_id))
		post = post_key.get()

		post.title = self.request.get('title')
		post.content = self.request.get('content')
		post.put()

		self.redirect('/')


class DeletePostHandler(BlogHandler):
	""" 
		Handler to delete the blog post
	"""
	def get(self, post_id):

		user_id = self.read_secure_cookie('user')

		# Takes user to the login page if he/she is not signed-in
		if not user_id:
			self.redirect('/login')

		else:
			author_key = ndb.Key('User', int(user_id))
			post_key = ndb.Key('Post', int(post_id))
			post = post_key.get()
			# Only author is allowed to delete the post
			if author_key != post.author:
				error_permission = "You are not allowed to delete this post"
				self.render('post.html', post=post, error_permission=error_permission)

			else:
				post_key = ndb.Key('Post', int(post_id))
				post_key.delete()

				self.redirect('/')


class PostPageHandler(BlogHandler):
	"""
		Handler to display each individual post
	"""
	def get(self, post_id):
		post_key = ndb.Key('Post', int(post_id))
		post = post_key.get()
		
		comments = Comment.query(Comment.post == post_key).fetch()

		self.render('post.html', post=post, comments=comments)
