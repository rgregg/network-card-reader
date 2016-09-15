import jsonstruct
import sys

class AppConfig:
    auth_authority_url = "https://login.microsoftonline.com/common"
    client_id = ""
    api_base_url = "https://graph.microsoft.com/beta"
    resource_url = "https://graph.microsoft.com"
    list_relative_path = ""
    username = "",
    password = ""
    verify_ssl = False
    access_token = ""

    @staticmethod
    def read_from_file():
        try:
            with open('config.json') as data_file:
                return jsonstruct.decode(data_file.read(), AppConfig)
        except Exception as err:
            print "Unable to parse config.json: %s" % err.message
            sys.exit()
