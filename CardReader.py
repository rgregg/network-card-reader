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
        self.site_id = None
        self.list_ids = {}

    def refresh_card_list(self):
        # graph.microsoft.com/beta/sharePoint/sites/{site-id}/lists/{list-id}/items?$select=id,listItemId&$expand=columnSet
        response_data = self.graph_request('GET', '/sharePoint/sites/' + self.site_id + '/lists/' + self.list_ids['Access Cards'] + '/items?$select=id,listItemId&$expand=columnSet')
        self.card_serials = {}
        for item in response_data['value']:
            column_set = item['columnSet']
            item_id = item['listItemId']
            card_serial_number = column_set['Card_x0020_Serial']
            self.card_serials[card_serial_number] = item_id

    def create_list_item(self):
        # Currently the API only allows creating empty items. This will be fixed in the future.
        # POST graph.microsoft.com/beta/sharePoint/sites/{site-id}/lists/{list-id}/items
        response_data = self.graph_request(
            'POST', 
            '/sharePoint/sites/' + self.site_id + '/lists/' + self.list_ids['Entry Log'] + '/items',
            '{}')
        return Models.ListItem(response_data)

    def patch_columns(self, item):
        # PATCH graph.microsoft.com/beta/sharePoint/sites/{site-id}/lists/{list-id}/items/{item-id}/columnSet
        response_data = self.graph_request(
            'PATCH',
            '/sharePoint/sites/' + self.site_id + '/lists/' + self.list_ids['Entry Log'] + '/items/' + item.id + '/columnSet',
            json.dumps(item.column_set))
        return Models.ListItem(response_data)

    def record_card_scan(self, card_number):
        # Look up the CardSerialId value from the list of valid cards
        card_id = self.card_serials[card_number]

        # add a new listitem to the list
        item = self.create_list_item()

        # update the list item with our values
        item.column_set = {
            'Entry_x0020_Time': datetime.datetime.utcnow().isoformat() + 'Z',
            'Title': 'Scanned at Reader 01 - %s' % card_number,
            'Card_x0020_SerialId': card_id
        }
        
        # Patch the list item with our new values
        self.patch_columns(item)





    def graph_request(self, method, relative_url, data=None):
        # Make sure last_token is valid
        self.last_token.refresh_token(self.config)

        url = self.config.api_base_url + relative_url
        headers = { 'Authorization': 'Bearer ' + self.last_token.access_token,
                    'Accept': 'application/json; odata.metadata=none',
                    'Content-Type': 'application/json' }
        try:
            if data is not None:
                print(method, url, '\n', data)
                r = requests.request(method, url, headers=headers, verify=self.config.verify_ssl, data=data)
            else:
                print(method, url)
                r = requests.request(method, url, headers=headers, verify=self.config.verify_ssl)
                
            r.raise_for_status()

            return r.json()
        except Exception as err:
            print('Unable to complete request.', url, 'error:', err)
        return None        
    def lookup_card_id(self, card_number):
        if card_number in self.card_serials:
            return self.card_serials[card_number]
        return None

    
    def cancel(self):
        self.run = False
        self.reader.close_input_device()
        print('Card reader shutdown.')

    def main(self):
        self.reader = RFIDReader.RfidCardReader()
        self.reader.open_input_device()

        print('Initializing...')
        self.resolve_list_ids()
        self.refresh_card_list()

        print('Card reader initialized.')

        while self.run:
            print('Waiting for card to scan.')

            # Try to read the card, if present
            card_number = self.reader.read_input()

            if card_number is not None:
                print('Card %s detected.' % card_number)
                self.record_card_scan(card_number)
            else:
                print('No card number detected. Aborting.')
                self.run = False
    
    def resolve_site_id(self):
        # This method is only necessary because of a bug in Graph /beta/ where the relative URL syntax doesn't
        # allow additional navigation beyond the end of the path. This will be fixed in the future and the  
        # API calls below can just use the relative URL instead of the IDs
        try:
            self.last_token.refresh_token(self.config)
        except Exception as err:
            print('Unable to refresh access token. %s' % err)

        url = self.config.api_base_url + '/sharePoint:' + self.config.site_relative_path
        headers = { 'Authorization': 'Bearer ' + self.last_token.access_token }
        print('GET', url)
        try:
            r = requests.get(url, headers=headers, verify=self.config.verify_ssl)
            r.raise_for_status()
            print('Site ID: %s' % r.json()['id'])
            return r.json()['id']
        except Exception as err:
            print('Error occured while getting site: %s' % err)
        return None
    
    def resolve_list_ids(self):
        # This method is only necessary because of a bug in Graph /beta/ where the relative URL syntax doesn't
        # allow additional navigation beyond the end of the path. This will be fixed in the future and the  
        # API calls below can just use the relative URL instead of the IDs

        try:
            self.last_token.refresh_token(self.config)
        except Exception as err:
            print('Unable to refresh access token. %s' % err)

        site_id = self.resolve_site_id()
        if not site_id:
            print('Unable to find site ID for relative URL')
            return None
        
        self.site_id = site_id

        url = self.config.api_base_url + '/sharePoint/sites/' + site_id + '/lists?$filter=name eq \'Access Cards\' or name eq \'Entry Log\''
        headers = { 'Authorization': 'Bearer ' + self.last_token.access_token }
        
        try:
            print('Request: GET %s' % url)
            r = requests.get(url, headers=headers, verify=self.config.verify_ssl)
            r.raise_for_status()
            
            lists = r.json()['value']
            for list in lists:
                name = list['name']
                id = list['id']
                self.list_ids[name] = id 
                print('Found list: ', name, ' == ', id)
        except HTTPError as err:
            print('Unsuccessful HTTP response: %s' % err)
        except Exception as err:
            print('Error occured while getting site: %s' % err)
        return None



def end_read(sig, frame):
    if sig == signal.SIGINT:
        print('\nCtrl+C captured, aborting.')
        if CardReaderSingleton.card_reader is not None:
            CardReaderSingleton.card_reader.cancel()

class CardReaderSingleton(object):
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

