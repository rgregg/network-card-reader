
## refresh_card_list

```python
        response_data = self.graph_request('GET', '')
        self.card_serials = {}
        for item in response_data['value']:
            column_set = item['columnSet']
            item_id = item['listItemId']
            card_serial_number = column_set['Card_x0020_Serial']
            self.card_serials[card_serial_number] = item_id
```


## create_list_item

```python
        response_data = self.graph_request(
            'POST', 
            '/sharePoint/sites/' + self.site_id + '/lists/' + self.list_ids['Entry Log'] + '/items',
            '{}')
        return Models.ListItem(response_data)
```


## patch_columns

```python
        response_data = self.graph_request(
            'PATCH',
            '/sharePoint/sites/' + self.site_id + '/lists/' + self.list_ids['Entry Log'] + '/items/' + item.id + '/columnSet',
            json.dumps(item.column_set))
        return Models.ListItem(response_data)
```


## record_card_scan

```python
        # Look up the card_number value from card_serials to get the card_id
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
```