import os
import webapp2
import jinja2
import hmac

from google.appengine.ext.webapp import template

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def render_str(template, **params):
	"""
		Function to render html
	"""
    t = jinja_env.get_template(template)
    return t.render(params)

def make_secure_val(val):
	"""
		Hash the password
	"""
	secret_key = "9834r381321314453"
	new_hash = hmac.new(secret_key, val).hexdigest()
	return "%s|%s" %(val, new_hash)

def check_secure_val(h):
	"""
		Check if the two hashed value matches
	"""
	s = h.split('|')[0]

	if h == make_secure_val(s):
		return s
