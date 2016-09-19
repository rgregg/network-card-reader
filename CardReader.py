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

import requests
import signal
import datetime
import json

import AppConfig
import AccessToken
import Models
import RFIDReader

class CardReader:
    def __init__(self):
        self.run = True
        self.last_token = AccessToken.AccessToken()
        self.config = AppConfig.AppConfig.read_from_file()

        # Allow overriding the access_token for debugging purposes
        if self.config.access_token:
            self.last_token.access_token = self.config.access_token
            self.last_token.expires = datetime.datetime.max


    def record_card_scan(self, card_number):
        # Make sure we have a fresh access token that works
        try:
            self.last_token.refresh_token(self.config)
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
            r = requests.post(url, data=data, headers=headers, verify=self.config.verify_ssl)
            r.raise_for_status()
            return Models.ListItem(r.json())
        except requests.HTTPError as err:
            print 'HTTP error creating a new item: %s' % err.message
        except Exception as err:
            print 'Error occured while creating an item %s' % err.message 
        return None

    def update_columns(self, item):
        url = self.config.api_base_url + '/sharepoint:' + self.config.list_relative_path + ':/items/' + item.id + '/columnSet'
        headers = { 'Authorization': 'Bearer ' + self.last_token.access_token,
                    'Content-Type': 'application/json' }
        try:
            r = requests.patch(url, json=item.column_set, headers=headers, verify=config.verify_ssl)
            r.raise_for_status()
            return Models.ListItem(r.json())
        except requests.HTTPError as err:
            print 'HTTP error creating a new item: %s' % err.message
        except Exception as err:
            print 'Error occured while creating an item %s' % err.message 
        return None
    
    def cancel(self):
        self.run = False
        self.reader.close_input_device()
        print 'Card reader shutdown.'

    def main(self):
        self.reader = RFIDReader.RfidCardReader()
        self.reader.open_input_device()

        print 'Card reader initialized. Waiting for card.'

        while self.run:
            # Try to read the card, if present
            # card_number = raw_input('Enter a card number: ')
            card_number = self.reader.read_input() 
            print 'Detected card number: %s' % card_number

            if card_number:
                print 'Card %s detected.' % card_number
                self.record_card_scan(card_number)
            else:
                print 'No card number detected. Aborting.'
                run = False
        
reader = CardReader()

def end_read(sig, frame):
    if sig == signal.SIGINT:
        print '\nCtrl+C captured, aborting.'
        reader.cancel()

if __name__ == '__main__':
    # Setup for Ctrl-C capture
    signal.signal(signal.SIGINT, end_read)

    # Run the main run loop
    reader.main()

    


