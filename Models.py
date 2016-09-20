'''
------------------------------------------------------------------------------
 Copyright (c) 2015 Microsoft Corporation
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

class BaseObject(object):
    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
    DATETIME_FORMAT_NO_MILLISECONDS = '%Y-%m-%dT%H:%M:%SZ'

    def to_dict(self):
        '''Returns the serialized form of the :class:`BaseObject`
        as a dict. All sub-objects that are based off of :class:`BaseObject`
        are also serialized and inserted into the dict
        
        Returns:
            dict: The serialized form of the :class:`OneDriveObjectBase`
        '''
        serialized = {}

        for prop in self._prop_dict:
            if isinstance(self._prop_dict[prop], OneDriveObjectBase):
                serialized[prop] = self._prop_dict[prop].to_dict()
            else:
                serialized[prop] = self._prop_dict[prop]

        return serialized
    
    @staticmethod
    def get_datetime_from_string(s):
        try:
            dt = datetime.strptime(
                s,
                BaseObject.DATETIME_FORMAT)
        except ValueError as ve:
            # Try again with other format
            dt = datetime.strptime(
                s,
                BaseObject.DATETIME_FORMAT_NO_MILLISECONDS)
        return dt
        
    @staticmethod
    def get_string_from_datetime(dt):
        return dt.strftime(BaseObject.DATETIME_FORMAT)        


class Identity(BaseObject):
    def __init__(self, prop_dict={}):
        self._prop_dict = prop_dict
        self.id_ = ''
        self.displayName = ''

    @property
    def id(self):
        if 'id' in self._prop_dict:
            return self._prop_dict['id']
        else:
            return None 

    @id.setter
    def id(self, val):
        self._prop_dict['id'] = val

    @property
    def display_name(self):
        if 'displayName' in self._prop_dict:
            return self._prop_dict['displayName']
        else:
            return None
    
    @display_name.setter
    def display_name(self, val):
        self._prop_dict['displayName'] = val

class IdentitySet(BaseObject):
    def __init__(self, prop_dict={}):
        self._prop_dict = prop_dict

    @property
    def user(self):
        if 'user' in self._prop_dict:
            if isinstance(self._prop_dict['user'], BaseObject):
                return self._prop_dict['user']
            else :
                self._prop_dict['user'] = Identity(self._prop_dict['user'])
                return self._prop_dict['user']
        return None

    @user.setter
    def user(self, val):
        self._prop_dict['user'] = val    

class ItemReference(BaseObject):
    def __init__(self, prop_dict={}):
        self._prop_dict = prop_dict
    
    @property
    def id(self):
        if 'id' in self._prop_dict:
            return self._prop_dict['id']
        else:
            return None 

    @id.setter
    def id(self, val):
        self._prop_dict['id'] = val        

class ListItem(BaseObject):
    def __init__(self, prop_dict={}):
        self._prop_dict = prop_dict
    
    # id property
    @property
    def id(self):
        if 'id' in self._prop_dict:
            return self._prop_dict['id']
        else:
            return None

    @id.setter
    def id(self, val):
        self._prop_dict['id'] = val

    # createdBy property
    @property
    def created_by(self):
        if 'createdBy' in self._prop_dict:
            if isinstance(self._prop_dict['createdBy'], BaseObject):
                return self._prop_dict['createdBy']
            else :
                self._prop_dict['createdBy'] = IdentitySet(self._prop_dict['createdBy'])
                return self._prop_dict['createdBy']

        return None

    @created_by.setter
    def created_by(self, val):
        self._prop_dict['createdBy'] = val

    # createdDateTime property        
    @property
    def created_date_time(self):
        if 'createdDateTime' in self._prop_dict:
            return self.get_datetime_from_string(self._prop_dict['createdDateTime'])
        else:
            return None

    @created_date_time.setter
    def created_date_time(self, val):
        self._prop_dict['createdDateTime'] = self.get_string_from_datetime(val)

    # eTag property
    @property
    def e_tag(self):
        if 'eTag' in self._prop_dict:
            return self._prop_dict['eTag']
        else:
            return None

    @e_tag.setter
    def e_tag(self, val):
        self._prop_dict['eTag'] = val    


    # lastModifiedBy property
    @property
    def last_modified_by(self):
        if 'lastModifiedBy' in self._prop_dict:
            if isinstance(self._prop_dict['lastModifiedBy'], BaseObject):
                return self._prop_dict['lastModifiedBy']
            else :
                self._prop_dict['lastModifiedBy'] = IdentitySet(self._prop_dict['lastModifiedBy'])
                return self._prop_dict['lastModifiedBy']

        return None

    @last_modified_by.setter
    def last_modified_by(self, val):
        self._prop_dict['lastModifiedBy'] = val

    # lastModifiedDateTime property
    @property
    def last_modified_date_time(self):
        if 'lastModifiedDateTime' in self._prop_dict:
            return self.get_datetime_from_string(self._prop_dict['lastModifiedDateTime'])
        else:
            return None

    @last_modified_date_time.setter
    def last_modified_date_time(self, val):
        self._prop_dict['lastModifiedDateTime'] = self.get_string_from_datetime(val)

    # listItemId property
    @property
    def list_item_id(self):
        if 'listItemId' in self._prop_dict:
            return self._prop_dict['listItemId']
        else:
            return None

    @list_item_id.setter
    def list_item_id(self,val):
        self._prop_dict['listItemId'] = val

    # parentReference property
    @property
    def parent_reference(self):
        if 'parentReference' in self._prop_dict:
            if isinstance(self._prop_dict['parentReference'], BaseObject):
                return self._prop_dict['parentReference']
            else :
                self._prop_dict['parentReference'] = ItemReference(self._prop_dict['parentReference'])
                return self._prop_dict['parentReference']

        return None

    @parent_reference.setter
    def parent_reference(self, val):
        self._prop_dict['parentReference'] = val

    # webUrl property
    @property
    def web_url(self):
        if 'webUrl' in self._prop_dict:
            return self._prop_dict['webUrl']
        else:
            return None

    @web_url.setter
    def web_url(self, val):
        self._prop_dict['webUrl'] = val    

    # columnSet property
    @property
    def column_set(self):
        if 'columnSet' in self._prop_dict:
            return self._prop_dict['columnSet']
        else:
            return None

    @column_set.setter
    def column_set(self,val):
        self._prop_dict['columnSet'] = val
