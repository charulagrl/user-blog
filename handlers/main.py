import webapp2

from models import Post
from google.appengine.ext import ndb
from utils import render_str, make_secure_val, check_secure_val

class BlogHandler(webapp2.RequestHandler):

    """ 
        Parent handler of all the other handlers which contains common functions 
    """

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
    	self.set_secure_cookie('user', str(user.key.id()))

    def logout(self):
    	self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % ('user', ''))


class MainPage(BlogHandler):
    """
        Handler to display front page of website
    """
    def get(self):

    	posts = Post.query().fetch()

        # Displays all the posts on the front page
        self.render('main.html', posts=posts)


class WelcomeHandler(BlogHandler):
    """
        Displays welcome page for user when user logs in
    """
    def get(self):

        user_id = self.read_secure_cookie('user')
        user = ndb.Key('User', int(user_id)).get()

        self.render("welcome.html", user=user)
