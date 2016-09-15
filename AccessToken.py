import datetime
import requests
import AppConfig

class AccessToken:
    access_token = ""
    expires = datetime.datetime.utcnow()
    app_config = None

    def expired(cls):
        if not cls.access_token:
            return True
        safe_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        if safe_date > cls.expires:
            return True
        return False
    
    def get_access_token(self, config):
        app_config = config
        r = requests.post(app_config.auth_authority_url + "/oauth2/token", data = {
            "resource": app_config.resource_url,
            "client_id": app_config.client_id,
            "grant_type": "password",
            "username": app_config.username,
            "password": app_config.password,
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