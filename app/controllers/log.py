import cgi
import logging
import jinja2
import os
import webapp2

from google.appengine.api import users
from app.swimitator import parse

basepath = os.path.dirname(__file__)
path = os.path.abspath(os.path.join(basepath, '..', 'templates'))

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(path))

def prepare_user_info(request):
    if users.get_current_user():
        url = users.create_logout_url(request.uri)
        url_linktext = 'Logout'
    else:
        url = users.create_login_url(request.uri)
        url_linktext = 'Login'
    
    template_values = {
        'url' : url,
        'url_linktext' : url_linktext
    }
    return template_values
    
class LogPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('log.html')
        self.response.out.write(template.render(prepare_user_info(self.request)))

app = webapp2.WSGIApplication([('/log', LogPage)])
