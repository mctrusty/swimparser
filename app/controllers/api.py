from datetime import datetime
import webapp2
import jinja2
import os

from google.appengine.api import users
from app.swimitator import parse
from app.models.workout import Workout

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
            
class InputWorkout(webapp2.RequestHandler):
    '''
    Data service that takes basic workout parameters and enters that workout into the database.
    '''
    def post(self):
        # Validate input. For now it comes from  Form data. 
        if 'workout' not in self.request.POST:
            self.response.write("Workout not in form")
        else:
            try:
                workout = self.request.get('workout')
                res = parse.get_json(workout)
            except:
                self.response.write('Invalid Workout Format<br/>')
        
        if 'date' not in self.request.POST:
            self.response.write('Date not in form<br/>')
        else:
            date = self.request.get('date')
            try:
                date = datetime.strptime(date, '%m/%d/%Y')
            except:
                self.response.write('Date format incorrect. Should be mm/dd/YYYY<br/>')
        
        #check for valid user
        if users.get_current_user():
            user = users.get_current_user()
        else:
            self.response.write('No user found. Please login or provide valid user credentials<br/>')
                
        # enter workout into database
        try:
            new_workout = Workout(user = user, date = date, workout = res)
            new_workout.put()
            self.response.write('Success')
        except:
            self.response.write('Workout write failed.<br/>')