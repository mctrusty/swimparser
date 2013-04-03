import unittest
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
		
	def tearDown(self):
		self.testbed.deactivate()
		
	@unittest.expectedFailure
	def test_basic_workout(self):
		self.assertEqual(1,0, 'add tests!')
		
	