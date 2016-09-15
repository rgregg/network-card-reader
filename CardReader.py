TOKEN_END_POINT = "https://login.microsoftonline.com/common/oauth2/token"
CLIENT_ID = "371758be-f5a9-4798-b405-1a10be9fa453"
RESOURCE_URL = "https://graph.microsoft.com"
API_BASE_URL = "https://graph.microsoft.com/beta"
USERNAME = "rgregg@odspdevelopers.com"
PASSWORD = "RRWPDuGI5MpH"
LIST_PATH = "/sites/1drvplat-ppe/lists/scan%20log"

run = True

import requests
import signal
import json
import datetime

class AccessToken:
    access_token = ""
    expires = datetime.datetime.utcnow()

    def expired(cls):
        if not cls.access_token:
            return True
        safe_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        if safe_date > cls.expires:
            return True
        return False

last_token = AccessToken()

def get_access_token(tokenEndPoint, resourceUrl, clientId, username, password):
    r = requests.post(tokenEndPoint, data = {
        "resource": resourceUrl,
        "client_id": clientId,
        "grant_type": "password",
        "username": username,
        "password": password,
        "scope": "openid"
        },
        verify = False)
    r.raise_for_status()
    
    val = AccessToken()
    json = r.json()
    val.access_token = json["access_token"]
    val.expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(json["expires_in"]))
    return val

def end_read(signal, frame):
    global run
    print("\nCtrl+C captured, ending card reading mode.")
    run = False

def refresh_access_token():
    global last_token
    if last_token.expired():
        print "Refreshing access_token..."
        last_token = get_access_token(TOKEN_END_POINT, RESOURCE_URL, CLIENT_ID, USERNAME, PASSWORD)
        if last_token.expired():
            print "Unable to generate a new access token. Scan cancelled."
            return False
        else:
            print "New access token: %s" % last_token.access_token
    return True

def record_card_scan(card_number):
    if refresh_access_token():
        # Record the card back to SharePoint
        url = API_BASE_URL + "/sharepoint:" + LIST_PATH + ":/items"
        headers = { "Authorization": "Bearer " + last_token.access_token,
                    "Content-Type": "application/json" }
        data = { }
        
        try:
            r = requests.post(url, json = data, headers = headers, verify=False)
            r.raise_for_status()
            return True
        except requests.HTTPError as err:
            print "Error making HTTP request: %s" % err.message
            

    return False

def main():
    global run

    # Setup for Ctrl-C capture
    signal.signal(signal.SIGINT, end_read)
    
    
    while run:

        # Try to read the card, if present
        card_number = raw_input("Enter a card number: ")
        if card_number:
            print "Card %s detected." % card_number
            result = record_card_scan(card_number)
            if result:
                print "Scan recorded."
            else:
                print "Failed to record scan."
        else:
            print "No card number detected. Aborting."
            run = False
main()


