from .eLABJournalObject import *

class Study(eLABJournalObject):

    def __init__(self, api, data):
        """
        Internal use only: initialize study object
        """
        if ((data is not None) & (type(data) == dict) & 
            ("name" in data)
           ):
            super().__init__(api, data, "studyID", str(data["name"])) 
        else:
            raise Exception("no (valid) study data")             