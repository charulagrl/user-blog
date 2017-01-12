import webapp2
from handlers import main, signup, post, login, logout, like, comment


app = webapp2.WSGIApplication([
    ('/', main.MainPage),
    ('/post/newpost', post.CreatePostHandler),
    ('/post/like/([0-9]+)', like.LikeHandler),
    ('/post/delete/([0-9]+)', post.DeletePostHandler),
    ('/post/edit/([0-9]+)', post.EditPostHandler),
    ('/post/comment/([0-9]+)', comment.CreateCommentHandler),
    ('/post/([0-9]+)', post.PostPageHandler),
    ('/signup', signup.SignupHandler),
    ('/login', login.LoginHandler),
    ('/logout', logout.LogoutHandler),
    ('/welcome', main.WelcomeHandler)
], debug=True)
