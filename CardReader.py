import requests
import signal
import jsonstruct
import datetime

import AppConfig
import AccessToken
import ListItem
import RFIDReader

class CardReader:
    def __init__(self):
        self.run = True
        self.last_token = AccessToken.AccessToken()
        self.config = AppConfig.AppConfig.read_from_file()

        # Allow overriding the access_token for debugging purposes
        if config.access_token:
            self.last_token.access_token = config.access_token
            self.last_token.expires = datetime.datetime.max


    def record_card_scan(self, card_number):
        # Make sure we have a fresh access token that works
        try:
            self.last_token.refresh_token(config)
        except Exception as err:
            print 'Unable to refresh access token. %s' % err.message

        item = self.create_list_item()
        if item:
            item.columnSet = {
                'Card_x0020_Unique_x0020_ID': card_number,
                'Entry_x0020_Time': datetime.datetime.utcnow().isoformat(),
                'Title': 'Badge Scanned'
            }
            self.update_columns(item)
        else:
            print 'Unable to create a new item in the list.'

    def create_list_item(self):
        url = self.config.api_base_url + '/sharepoint:' + self.config.list_relative_path + ':/items'
        headers = { 'Authorization': 'Bearer ' + self.last_token.access_token,
                    'Content-Type': 'application/json' }
        data = '{}'
        
        try:
            r = requests.post(url, data=data, headers=headers, verify=config.verify_ssl)
            r.raise_for_status()
            return jsonstruct.decode(r.text, ListItem.ListItem)
        except requests.HTTPError as err:
            print 'HTTP error creating a new item: %s' % err.message
        except Exception as err:
            print 'Error occured while creating an item %s' % err.message 
        return None

    def update_columns(self, item):
        url = self.config.api_base_url + '/sharepoint:' + self.config.list_relative_path + ':/items/' + item.id + '/columnSet'
        headers = { 'Authorization': 'Bearer ' + self.last_token.access_token,
                    'Content-Type': 'application/json' }
        data = jsonstruct.encode(item.columnSet)
        
        try:
            r = requests.patch(url, data=data, headers=headers, verify=config.verify_ssl)
            r.raise_for_status()
            return jsonstruct.decode(r.text, ListItem)
        except requests.HTTPError as err:
            print 'HTTP error creating a new item: %s' % err.message
        except Exception as err:
            print 'Error occured while creating an item %s' % err.message 
        return None
    
    def cancel(self):
        self.run = False
        self.reader.close_input_device()

    def run(self):
        self.reader = RFIDReader.RfidCardReader()
        self.reader.open_input_device()

        while self.run:
            # Try to read the card, if present
            # card_number = raw_input('Enter a card number: ')
            card_number = self.reader.read_input() 

            if card_number:
                print 'Card %s detected.' % card_number
                record_card_scan(card_number, last_token)
            else:
                print 'No card number detected. Aborting.'
                run = False
        
reader = CardReader()
if __name__ == '__main__':
    # Setup for Ctrl-C capture
    signal.signal(signal.SIGINT, self.end_read)

    # Run the main run loop
    reader.run()

def end_read(signal, frame):
    if (signal == signal.SIGINT)
        print '\nCtrl+C captured, aborting.'
        reader.cancel()
    


