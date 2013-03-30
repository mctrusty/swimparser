import cgi
import logging
import jinja2
import os
import webapp2

from app.controllers.index import *

def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('Oops! I could swear this page was here!')
    response.set_status(404)

def handle_500(request, response, exception):
    logging.exception(exception)
    response.write('A server error occurred!\n\n')
    if exception.detail:
        response.write(exception.detail)
    response.set_status(500)
    
app = webapp2.WSGIApplication([('/', MainPage),
							   ('/contact', ContactPage),
							   ('/about', AboutPage),
                               ('/parse', Parse)],
                               debug=True)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500
