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
            
    def studies(self, *args, **kwargs):
        """
        Get object to access experiments within this study.
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
        sort : str, optional    
            Sort by a specific field
        studyID : str, optional
            Filter by studyID
        search : str, optional
            Search experiments by name or contents
        """    
        request = {"projectID": self.id()}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["studyID", "search"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
                    check_arg = arg.first(True)
                raise Exception("unsupported object '"+str(type(check_arg))+"'")                 
        if kwargs is not None:
            for key, value in kwargs.items():
                if key in kwargs_special:
                    request[key] = value   
                elif key in kwargs_keys:
                    request[key] = value
                else:
                    raise Exception("unsupported key '"+key+"'")                   
        return self._eLABJournalObject__api.studies(**request)
        
    