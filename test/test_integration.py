"""Tests that content can be retrieved from a simple application."""

PATH_TO_THE_APP_ENGINE_SDK = 'C:\Program Files (x86)\Google\google_appengine'
import sys; sys.path.insert(0, PATH_TO_THE_APP_ENGINE_SDK)
import unittest
import os.path

import regtest_utils


class TestIntegration(regtest_utils.BaseTestCase):
  """Tests that content can be retrieved from a simple application."""

  def setUp(self):
    super(TestIntegration, self).setUp()
    server_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'app.yaml'))
    self.start_server([server_path])

  def test_hello(self):
    status, content, headers = self.fetch_url('default', 'GET', '/')
    self.assertEqual(200, status)
#    self.assertEqual('Hello!', content)
    self.assertEqual('text/plain', headers['Content-Type'])

  def test_log_restricted(self):
    status, content, headers = self.fetch_url('default', 'GET', '/log')
    self.assertEqual(302, status)
    
  def test_404(self):
    status, _, _ = self.fetch_url('default',
                                  'GET',
                                  '/foo')
    self.assertEqual(404, status)

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIntegration)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
if __name__ == '__main__':
  main()
