import pdb
import sys
sys.path.append("..")
sys.path.append("C:\\Users\\mjcox\\Documents\\Swimitator\\swimparser")

import unittest
import webapp2
from webtest import TestApp
import swim
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

class LogTest(unittest.TestCase):
    
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        # Set consistency policy to simulate HR consistency model
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=0)
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
        self.testbed.init_user_stub()
        
    def tearDown(self):
        self.testbed.deactivate()
        
    def test_log_requires_login(self):
        ''' Make sure attempted access redirects to a login page '''
        app = TestApp(swim.app)
        #response = app.get('/log')
        request = webapp2.Request.blank('/log')
        response = request.get_response(swim.app)
        #response = app.get('/log')
		#pdb.set_trace()
        self.assertEqual(response.status_int, 302)
        self.assertEqual(response.body, 'Requires login')
    
    @unittest.expectedFailure
    def test_basic_workout(self):
        self.assertEqual(1,0, 'add tests!')
        
    