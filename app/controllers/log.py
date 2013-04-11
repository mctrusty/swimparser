import pdb
import cgi
import logging
import jinja2
import os
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users
from app.swimitator import parse
from app.models.workout import Workout

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
        pdb.set_trace()
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

class LogView(webapp2.RequestHandler):
    def get(self):
        workouts = ndb.gql("SELECT * from Workout WHERE user = :1", users.get_current_user())
        template_values = prepare_user_info(self.request)
        template_values['workouts'] = workouts
        template = jinja_environment.get_template('log-view.html')
        self.response.out.write(template.render(template_values))

