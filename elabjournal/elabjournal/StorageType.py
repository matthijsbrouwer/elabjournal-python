from .eLABJournalObject import *

class StorageType(eLABJournalObject):

    def __init__(self, api, data):
        """
        Internal use only: initialize storage object
        """
        if ((data is not None) & (type(data) == dict) & 
            ("name" in data)
           ):
            super().__init__(api, data, "storageTypeID", str(data["name"])) 
        else:
            raise Exception("no (valid) storage type data") 
            
    def storages(self):
        """
        Get storages for this storage type.
        """
        return self._eLABJournalObject__api.storages(storageTypeID=self.id())  
        
    def type(self):
        """
        Get deviceType.
        """
        data = self.data()
        if "deviceType" in data:
            return(data["deviceType"])
        else:
            return(None)                   
        
    