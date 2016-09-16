import datetime

class Identity(object):
    def __init__(self):
        self.id_ = ""
        self.displayName = ""

class IdentitySet(object):
    def __init__(self):
        self.user = Identity()

class ItemReference(object):
    def __init__(self):
        self.id_ = ""

class ListItem(object):
    def __init__(self):
        self.id_ = ""
        self.createdBy = IdentitySet()
        self.createdDateTime = ""
        self.eTag = ""
        self.lastModifiedBy = IdentitySet()
        self.lastModifiedDateTime = ""
        self.listItemId = 0
        self.parentReference = ItemReference()
        self.webUrl = ""
        self.columnSet = { }

