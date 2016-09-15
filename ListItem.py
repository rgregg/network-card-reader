import datetime

class Identity(object):
    id = ""
    displayName = ""

class IdentitySet(object):
    user = Identity()

class ItemReference(object):
    id = ""

class ListItem(object):
    id = ""
    createdBy = IdentitySet()
    createdDateTime = ""
    eTag = ""
    lastModifiedBy = IdentitySet()
    lastModifiedDateTime = ""
    listItemId = 0
    parentReference = ItemReference()
    webUrl = ""
    columnSet = { }

