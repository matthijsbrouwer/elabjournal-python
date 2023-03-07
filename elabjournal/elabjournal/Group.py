from .eLABJournalObject import * 

class Group(eLABJournalObject):

    def __init__(self, api, data):        
        """
        Internal use only: initialize sample serie.
        """
        if ((data is not None) & (type(data) == dict) & 
            ("name" in data.keys())
           ):
            super().__init__(api, data, "groupID", str(data["name"])) 
        else:
            raise Exception("no (valid) Group data") 
          