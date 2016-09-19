'''
------------------------------------------------------------------------------
 Copyright (c) 2016 Microsoft Corporation
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
------------------------------------------------------------------------------
'''

import sys
import json

class AppConfig:

    def __init__(self, prop_dict={}):
        self._prop_dict = prop_dict

    @property
    def auth_authority_url(self):
        if "authAuthorityUrl" in self._prop_dict:
            return self._prop_dict["authAuthorityUrl"]
        else:
            return None
    
    @property
    def client_id(self):
        if "clientId" in self._prop_dict:
            return self._prop_dict["clientId"]
        else:
            return None

    @property
    def api_base_url(self):
        if "apiBaseUrl" in self._prop_dict:
            return self._prop_dict["apiBaseUrl"]
        else:
            return None

    @property
    def resource_url(self):
        if "resourceUri" in self._prop_dict:
            return self._prop_dict["resourceUri"]
        else:
            return None
    
    @property
    def list_relative_path(self):
        if "listRelativePath" in self._prop_dict:
            return self._prop_dict["listRelativePath"]
        else:
            return None
    
    @property
    def username(self):
        if "username" in self._prop_dict:
            return self._prop_dict["username"]
        else:
            return None
    
    @property
    def password(self):
        if "password" in self._prop_dict:
            return self._prop_dict["password"]
        else:
            return None
    
    @property
    def verify_ssl(self):
        if "verifySSL" in self._prop_dict:
            return self._prop_dict["verifySSL"]
        else:
            return None

    @property
    def access_token(self):
        if "accessToken" in self._prop_dict:
            return self._prop_dict["accessToken"]
        else:
            return None

    @staticmethod
    def read_from_file(named = 'config.json'):
        try:
            with open(named) as data_file:
                data = json.loads(data_file)
                return AppConfig(data)
        except Exception as err:
            print 'Unable to parse config.json: %s' % err.message
            sys.exit(1)
