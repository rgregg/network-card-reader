run = True

import requests
import signal
import jsonstruct
import datetime

import AppConfig
import AccessToken
import ListItem

last_token = AccessToken.AccessToken()
config = AppConfig.AppConfig.read_from_file()

# Allow overriding the access_token for debugging purposes
if config.access_token:
    last_token.access_token = config.access_token
    last_token.expires = datetime.datetime.max

def record_card_scan(card_number):
    
    # Make sure we have a fresh access token that works
    try:
        last_token.refresh_token(config)
    except Exception as err:
        print "Unable to refresh access token. %s" % err.message

    item = create_list_item()
    if item:
        item.columnSet = {
            "Card_x0020_Unique_x0020_ID": card_number,
            "Entry_x0020_Time": datetime.datetime.utcnow().isoformat(),
            "Title": "Badge Scanned"
        }
        update_columns(item)
    else:
        print "Unable to create a new item in the list."

def create_list_item():
    url = config.api_base_url + "/sharepoint:" + config.list_relative_path + ":/items"
    headers = { "Authorization": "Bearer " + last_token.access_token,
                "Content-Type": "application/json" }
    data = "{}"
    
    try:
        r = requests.post(url, data=data, headers=headers, verify=config.verify_ssl)
        r.raise_for_status()
        return jsonstruct.decode(r.text, ListItem.ListItem)
    except requests.HTTPError as err:
        print "HTTP error creating a new item: %s" % err.message
    except Exception as err:
        print "Error occured while creating an item %s" % err.message 
    return None

def update_columns(item):
    url = config.api_base_url + "/sharepoint:" + config.list_relative_path + ":/items/" + item.id + "/columnSet"
    headers = { "Authorization": "Bearer " + last_token.access_token,
                "Content-Type": "application/json" }
    data = jsonstruct.encode(item.columnSet)
    
    try:
        r = requests.patch(url, data=data, headers=headers, verify=config.verify_ssl)
        r.raise_for_status()
        return jsonstruct.decode(r.text, ListItem)
    except requests.HTTPError as err:
        print "HTTP error creating a new item: %s" % err.message
    except Exception as err:
        print "Error occured while creating an item %s" % err.message 
    return None

def main():
    global run

    # Setup for Ctrl-C capture
    signal.signal(signal.SIGINT, end_read)
    
    while run:

        # Try to read the card, if present
        card_number = "0316140010808056" # raw_input("Enter a card number: ")
        if card_number:
            print "Card %s detected." % card_number
            record_card_scan(card_number)
        else:
            print "No card number detected. Aborting."
            run = False

def end_read(signal, frame):
    global run
    print("\nCtrl+C captured, ending card reading mode.")
    run = False

main()


