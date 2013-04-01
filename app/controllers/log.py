import cgi
import logging
import jinja2
import os
import webapp2

from google.appengine.api import users
from app.swimitator import parse
from app.models.workout import Workout

basepath = os.path.dirname(__file__)
path = os.path.abspath(os.path.join(basepath, '..', 'templates'))

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(path))

class LogPage(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            user = users.get_current_user()
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            user = 'Anonymous'
            
        template_values = {
            'url' : url,
            'url_linktext' : url_linktext,
            'user' : user
        }

        template = jinja_environment.get_template('log.html')
        self.response.out.write(template.render(template_values))
       
#app = webapp2.WSGIApplication([('/log', LogPage)])
