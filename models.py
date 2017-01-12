from google.appengine.ext import ndb



class Post(ndb.Model):
	""" 
		Class for Post Modal
	"""
	title = ndb.StringProperty(required=True)
	content = ndb.StringProperty(required=True, indexed=False)
	author = ndb.KeyProperty(kind='User')
	like_count = ndb.IntegerProperty(default=0)
	date = ndb.DateTimeProperty(auto_now_add=True)

	def update_likes_count(self):
		"""
			On each like, update the likes count
		""" 
		self.like_count += 1
		self.put()


class User(ndb.Model):
	""" 
		Class for User Modal
	"""
	username = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)
	email = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)


class Like(ndb.Model):
	""" 
		Class for Like Modal
	"""
	post = ndb.KeyProperty(required=True)
	user = ndb.KeyProperty(required=True)
	date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_likes_count(self, post_key):
		""" 
			Query Likes object to get the count of likes for a post
		"""
		likes_count = Like.query(Like.post == post_key).count()
		return likes_count

	@classmethod
	def create_like(self, post_key, user_key):
		"""
			Create a like object. Do not like if the user has already liked the post.

		"""
		like = self.is_liked(post_key, user_key)

		if like:
			return
		else:
			like = Like(post=post_key, user=user_key)
			like.put()

			post = post_key.get()

			# Call the update likes count after each like object is created
			post.update_likes_count()

	@classmethod
	def is_liked(self, post_key, user_key):
		"""
			Checks if the post is already liked by a user
		"""
		like = Like.query(Like.user == user_key, Like.post == post_key).get()

		if like:
			return True
		else:
			return False


class Comment(ndb.Model):
	""" 
		Class for Like Modal
	"""

	content = ndb.StringProperty(required=True)
	post = ndb.KeyProperty(required=True)
	user = ndb.KeyProperty(required=True)
	date = ndb.DateTimeProperty(auto_now_add=True)
