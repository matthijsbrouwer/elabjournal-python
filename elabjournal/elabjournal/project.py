from .eLABJournalObject import * 

class Project(eLABJournalObject):

    def __init__(self, api, data):
        """
        Internal use only: initialize project object
        """
        if ((data is not None) & (type(data) == dict) & 
            ("name" in data)
           ):
            super().__init__(api, data, "projectID", str(data["name"])) 
        else:
            raise Exception("no (valid) project data") 
        
    