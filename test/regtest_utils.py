"""Utilities for creating development server regression tests."""

import httplib
import json
import logging
import os.path
import socket
import sys
import unittest
import wsgiref.headers

import dev_appserver
sys.path[1:1] = dev_appserver._DEVAPPSERVER2_PATHS

from google.appengine.api import apiproxy_stub_map
from google.appengine.tools.devappserver2 import devappserver2
from google.appengine.tools.devappserver2 import python_runtime


class BaseTestCase(unittest.TestCase):
  """A base class for all development server regression tests."""

  def setUp(self):
    # Reset the stub map between requests because a stub map only allows a
    # stub to be added once.
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    self.server = None

  def tearDown(self):
    if self.server:
      self.server.stop()

  def start_server(self, server_paths):
    """Starts the development server and assigns it to self.server.

    Args:
      server_paths: A list of strings representing the paths to the app.yaml
          files for the servers that should be run.
    """
    python_runtime._RUNTIME_ARGS = [
        sys.executable,
        os.path.join(
            os.path.dirname(dev_appserver.__file__), '_python_runtime.py')]
    options = devappserver2.PARSER.parse_args([
        '--admin_port', '0',
        '--port', '0',
        '--datastore_path', ':memory:',
        '--logs_path', ':memory:',
        '--skip_sdk_update_check',
        '--',
        ] + server_paths)
    self.server = devappserver2.DevelopmentServer()
    self.server.start(options)

  def retrieve_json_url(self, server, relative_url, headers=None, method='GET',
                        instance=None):
    """Returns the JSON response returned by sending a request to a server.

    Args:
      server: The name of the server that the request should be sent to e.g.
          "default".
      relative_url: The relative URL that should be accessed on the server
          e.g. "/foo?bar=baz".
      headers: A dict containing the headers that should be sent.
      method: A str containing the HTTP method to send. Defaults to GET.
      instance: A str containing the instance ID of the instance to send the
          request to. Defaults to using the load-balancer.

    Returns:
      The parsed JSON response returned by the server.
    """
    status, response, _ = self.fetch_url(server, method, relative_url,
                                         headers=headers, instance=instance)
    assert status == 200, 'unexpected status %d' % status
    try:
      return json.loads(response)
    except ValueError:
      logging.exception('Failed to parse invalid json: %r', response)
      raise

  def fetch_url(self,
                server,
                method,
                relative_url,
                body=None,
                headers=None,
                instance=None):
    """Makes an HTTP request to the given server and returns the result.

    Args:
      server: The name of the server that the request should be sent to e.g.
          "default".
      method: The HTTP method to use when fetching the URL e.g. "GET".
      relative_url: The URL to access on the server e.g. "/foo?bar=baz".
      body: The body to use in the HTTP request.
      headers: A dict containing the headers that should be sent.
      instance: A str containing the instance ID of the instance to send the
          request to. Defaults to using the load-balancer.

    Returns:
      A 3-tuple of:
        status: An int representing the received HTTP status code e.g. 200.
        content: A string containing the content of the HTTP reply.
        headers: A wsgiref.headers.Headers instance containing the received
            HTTP headers.
    """
    host = self.server.server_to_address(server, instance=instance)
    headers = headers or {}
    if not relative_url.startswith('/'):
      relative_url = '/' + relative_url

    logging.info('Connecting to %s', host)
    try:
      connection = httplib.HTTPConnection(host)

      logging.info('Sending request "%s %s"', method, relative_url)
      try:
        connection.putrequest(method, relative_url)

        if body is None:
          content_length = 0
        else:
          content_length = len(body)
        if method not in ('GET', 'TRACE') or content_length:
          connection.putheader('Content-length', content_length)

        for key, value in headers.iteritems():
          connection.putheader(str(key), str(value))
        connection.endheaders()

        if body is not None:
          connection.send(body)

        response = connection.getresponse()
        status = response.status
        content = response.read()

        # Ensures that we avoid merging repeat headers into a single header,
        # allowing use of multiple Set-Cookie headers.
        headers = []
        for name in response.msg:
          for value in response.msg.getheaders(name):
            headers.append((name, value))

        headers = wsgiref.headers.Headers(headers)
        logging.info('Received response %s with content:\n%s\n',
                     status,
                     content[:1024 * 16])

        return status, content, headers
      finally:
        connection.close()
    except (IOError, httplib.HTTPException, socket.error), e:
      logging.info('Encountered exception accessing HTTP server: %s', e)
      raise
