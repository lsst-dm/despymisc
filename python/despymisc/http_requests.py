"""Module providing an easy-to-use API for http requests to DESDM services.

Loads credentials from a desfile storing credentials (.desservices.ini, by
default assumed to be in the users home directory).

USAGE:
``````
- download DES file from address:
    http_requests.download_file_des('http://www.blabla.net/foo.xyz', 'blabla.xyz')

:author: michael h graber, michael.graber@fhnw.ch
"""

import os
import urllib.error
import urllib.parse
import urllib.request
from base64 import b64encode


def get_credentials(desfile=os.path.join(os.environ['HOME'], '.desservices.ini'),
                    section='http-desarchive'):
    """Load the credentials using serviceaccess from a local .desservices file.
    """

    try:
        from despyserviceaccess import serviceaccess
        creds = serviceaccess.parse(desfile, section)
        USERNAME = creds['user']
        PASSWORD = creds['passwd']
        URL = creds.get('url', None)
    except:
        USERNAME = None
        PASSWORD = None
        URL = None
        warning = """WARNING: could not load credentials from .desservices.ini file for section %s
        please make sure sections make sense""" % section
        print(warning)

    return USERNAME, PASSWORD, URL


def download_file_des(url, filename, desfile=None, section='http-desarchive'):
    """Download files using the DES services files.
    """
    # Get the credentials
    USERNAME, PASSWORD, URL = get_credentials(desfile=desfile, section=section)
    auth = (USERNAME, PASSWORD)
    req = Request(auth)
    req.download_file(url, filename)


class Request(object):
    """
    """

    def __init__(self, auth):

        # auth = (USERNAME, PASSWORD)
        self.auth = auth
        self.url = None
        self.response = None
        self.error_status = (False, '')

    def POST(self, url, data=None):
        """
        """
        if not type(data) == dict:
            raise ValueError(('The data kwarg needs to be set and of type '
                              'dictionary.'))
        else:
            self.data = data
        if not url:
            raise ValueError('You need to provide an url kwarg.')
        else:
            self.url = url

        urllib_req = urllib.request.Request(self.url)
        if any(self.auth):
            urllib_req.add_header('Authorization',
                                  'Basic ' + b64encode(self.auth[0]+':'+self.auth[1]))
        try:
            self.response = urllib.request.urlopen(urllib_req,
                                            urllib.parse.urlencode(self.data))
        except Exception as e:
            self.error_status = (True, str(e))

    def get_read(self, url):
        """
        """
        if not url:
            raise ValueError('You need to provide an url kwarg.')
        else:
            self.url = url

        urllib_req = urllib.request.Request(self.url)
        if any(self.auth):
            urllib_req.add_header('Authorization',
                                  'Basic ' + b64encode(self.auth[0]+':'+self.auth[1]))
        try:
            self.response = urllib.request.urlopen(urllib_req)
            return self.response.read()
        except Exception as e:
            self.error_status = (True, str(e))

    def download_file(self, url, filename):
        """
        """
        with open(filename, 'wb') as f:
            f.write(self.get_read(url))

    def GET(self, url, params={}):
        """
        """
        if not url:
            raise ValueError('You need to provide an url kwarg.')
        else:
            self.url = url

        url_params = '?'+'&'.join([str(k)+'='+str(v) for k, v in
                                   list(params.items())])
        urllib_req = urllib.request.Request(self.url+url_params)
        if any(self.auth):
            urllib_req.add_header('Authorization',
                                  'Basic ' + b64encode(self.auth[0]+':'+self.auth[1]))
        try:
            self.response = urllib.request.urlopen(urllib_req)
        except Exception as e:
            self.error_status = (True, str(e))
