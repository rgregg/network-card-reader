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

class CardReader(object):
    def __init__(self):
        self.run = True
        self.last_token = AccessToken.AccessToken()
        self.config = AppConfig.AppConfig.read_from_file()
        self.card_serials = {}

        # Allow overriding the access_token for debugging purposes
        if self.config.access_token:
            self.last_token.access_token = self.config.access_token
            self.last_token.expires = datetime.datetime.max

    def refresh_card_list(self):
        # Refresh the valid card numbers from the server
        try:
            self.last_token.refresh_token(self.config)
        except Exception as err:
            print('Unable to refresh access token. %s' % err.message)
        
        # /sharepoint:/path:/items?$select=id&$expand=columnSet($select=EmployeeId,Card_x0020_Serial)
        url = self.config.api_base_url + '/sharepoint:' + self.config.access_cards_path + ':/items?$select=id&$expand=columnSet($select=EmployeeId,Card_x0020_Serial)'
        headers = { 'Authorization': 'Bearer ' + self.last_token.access_token }

        try:
            r = requests.get(url, headers=headers, verify=self.config.verify_ssl)
            r.raise_for_status()

            self.card_serials = self.parse_card_list(r.json())

        except Exception as err:
            print('Unable to retrieve valid access cards. %s' % err.message)

    def parse_card_list(self, input_dict):
        if 'value' not in input_dict:
            raise ValueException('No values element in dict')

        output = {}
        values = input_dict['value']
        for item in values:
            try:
                if 'columnSet' not in item:
                    continue
                column_set = item['columnSet']
                employee_id = column_set['EmployeeId']
                card_serial = None
                if 'Card_x0020_Serial' in column_set:
                    card_serial = column_set['Card_x0020_Serial']
                elif 'Card_x005f_x0020_x005f_Serial' in column_set:
                    card_serial = column_set['Card_x005f_x0020_x005f_Serial']
                output[card_serial] = employee_id
            except Excetion as err:
                print('Unable to parse response item: %s' % err.message)
        
        return output
    
    def lookup_card_id(self, card_number):
        if card_number in self.card_serials:
            return self.card_serials[card_number]
        return None


    def record_card_scan(self, card_number):
        # Make sure we have a fresh access token that works
        try:
            self.last_token.refresh_token(self.config)
        except Exception as err:
            print('Unable to refresh access token. %s' % err.message)
        
        # Look up the CardSerialId value from the list of valid cards
        card_id = self.lookup_card_id(card_number)
        if card_id is None:
            print('Invalid card scanned. Access denied.')
            return

        item = self.create_list_item()
        if item:
            item.column_set = {
                'Entry_x0020_Time': datetime.datetime.utcnow().isoformat(),
                'Title': 'Scanned at Reader 01'
            }
            # 'Card_x0020_SerialId': card_id,
            self.update_columns(item)
        else:
            print('Unable to create a new item in the list.')

    def create_list_item(self):
        url = self.config.api_base_url + '/sharepoint:' + self.config.entry_log_path + ':/items'
        headers = { 'Authorization': 'Bearer ' + self.last_token.access_token,
                    'Content-Type': 'application/json' }
        data = '{}'
        
        try:
            r = requests.post(url, data=data, headers=headers, verify=self.config.verify_ssl)
            r.raise_for_status()
            return Models.ListItem(r.json())
        except requests.HTTPError as err:
            print('HTTP error creating a new item: %s' % err.message)
        except Exception as err:
            print('Error occured while creating an item %s' % err.message)
        return None

    def update_columns(self, item):
        url = self.config.api_base_url + '/sharepoint:' + self.config.entry_log_path + ':/items/' + item.id + '/columnSet'
        headers = { 'Authorization': 'Bearer ' + self.last_token.access_token,
                    'Content-Type': 'application/json' }
        try:
            r = requests.patch(url, json=item.column_set, headers=headers, verify=self.config.verify_ssl)
            r.raise_for_status()
            return Models.ListItem(r.json())
        except requests.HTTPError as err:
            print('HTTP error creating a new item: %s' % err.message)
        except Exception as err:
            print('Error occured while creating an item %s' % err.message)
        return None
    
    def cancel(self):
        self.run = False
        self.reader.close_input_device()
        print('Card reader shutdown.')

    def main(self):
        self.reader = RFIDReader.RfidCardReader()
        self.reader.open_input_device()

        print('Initializing...')
        self.refresh_card_list()

        print('Card reader initialized. Waiting for card.')

        while self.run:
            # Try to read the card, if present
            card_number = self.reader.read_input()

            if card_number is not None:
                print('Card %s detected.' % card_number)
                self.record_card_scan(card_number)
            else:
                print('No card number detected. Aborting.')
                run = False


def end_read(sig, frame):
    if sig == signal.SIGINT:
        print('\nCtrl+C captured, aborting.')
        if CardReaderSingleton.card_reader is not None:
            CardReaderSingleton.card_reader.cancel()

class CardReaderSingleton(object)
    card_reader = None
    
    @staticmethod
    def initialize_singleton():
        CardReaderSingleton.card_reader = CardReader()

if __name__ == '__main__':
    # Setup for Ctrl-C capture
    signal.signal(signal.SIGINT, end_read)
    
    # Init CardReaderSingleton
    CardReaderSingleton.initialize_singleton()
    
    # Run the main run loop
    CardReaderSingleton.card_reader.main()

