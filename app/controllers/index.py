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
    
class ContactPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('contact.html')
        self.response.out.write(template.render(prepare_user_info(self.request)))
    
class AboutPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('about.html')
        self.response.out.write(template.render(prepare_user_info(self.request)))

class LogPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('log.html')
        self.response.out.write(template.render(prepare_user_info(self.request)))
        
class MainPage(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        
        template_values = {
            'url' : url,
            'url_linktext' : url_linktext
        }
        
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

class Parse(webapp2.RequestHandler):
    def post(self):
        logging.debug('Starting Parse post request')
        format = self.request.get('format')
        format_string = '</pre><hr>' + format + '<pre>'
        self.response.out.write('<html><body>Workout:<pre>')
        self.response.out.write(cgi.escape(self.request.get('workout')))
        self.response.out.write(format_string)
        if format == 'xml':
            self.response.out.write(cgi.escape(self.print_workout_xml()))
        else:
            self.response.out.write(cgi.escape(self.print_workout_json()))
        self.response.out.write('</pre></body></html>')

    def print_workout_xml(self):
        workout = self.request.get('workout')
        logging.debug('workout',workout)
        try:
            res = parse.get_xml(workout)
        except:
            self.abort(500, detail='Parsing Error - please check workout syntax')
            
        return res
        
    def print_workout_json(self):
        workout = self.request.get('workout')
        logging.debug('workout',workout)
        try:
            res = parse.get_json(workout)
        except:
            self.abort(500, detail='Parsing Error - please check workout syntax')
            
        return res
