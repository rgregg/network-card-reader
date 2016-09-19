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

import datetime
import requests
import AppConfig

class AccessToken:
    
    def __init__(self):
        self.access_token = ""
        self.expires = datetime.datetime.utcnow()

    def expired(cls):
        if not cls.access_token:
            return True
        safe_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        if safe_date > cls.expires:
            return True
        return False
    
    def get_access_token(self, config):
        r = requests.post(config.auth_authority_url + "/oauth2/token", data = {
            "resource": config.resource_url,
            "client_id": config.client_id,
            "grant_type": "password",
            "username": config.username,
            "password": config.password,
            "scope": "openid"
            },
            verify = config.verify_ssl)
        r.raise_for_status()
        
        json = r.json()
        self.access_token = json["access_token"]
        self.expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(json["expires_in"]))

    def refresh_token(self, config):
        if self.expired():
            print "Refreshing access_token..."
            self.get_access_token(config)
            if self.expired():
                print "Unable to generate a new access token. Scan cancelled."
                return False
            else:
                print "New access token: %s" % self.access_token
        return True        