import webapp2
import jinja2
import os

from google.appengine.api import users
from app.swimitator import parse

#jinja2 set up
basepath = os.path.dirname(__file__)
path = os.path.abspath(os.path.join(basepath, '..', 'templates'))
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(path))

class JsonWorkout(webapp2.RequestHandler):
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

        template = jinja_environment.get_template('api.html')
        self.response.out.write(template.render(template_values))
        
    def post(self):
        workout = self.request.get('workout')
        if workout:
            res = parse.get_json(workout)
        else:
            res = 'no workout'
        self.response.write(res)