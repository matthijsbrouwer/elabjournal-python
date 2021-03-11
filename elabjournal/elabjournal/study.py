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
            
    def experiments(self, *args, **kwargs):
        """
        Get object to access experiments within this study.
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
        sort : str, optional    
            Sort by a specific field
        projectID : str, optional
            Filter by project   
        search : str, optional
            Search experiments by name or contents
        """    
        request = {"studyID": self.id()}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["search"]
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
        return self._eLABJournalObject__api.experiments(**request)
    
    def create_experiment(self, *args, **kwargs):
        """
        Create experiment
        
        Parameters (key/value)
        ----------------------
        name: str, required
            Name of the experiment 
        status: str, optional
            Status of the experiment 
        
        """ 
        request = {}
        required = {}
        kwargs_obligatory = ["name"]
        kwargs_keys = ["name","status"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
                    check_arg = arg.first(True)
                raise Exception("unsupported object '"+str(type(check_arg))+"'")                 
        if kwargs is not None:
            for key, value in kwargs.items():
                if key in kwargs_keys:
                    request[key] = value
                else:
                    raise Exception("unsupported key '"+key+"'") 
        for key in kwargs_obligatory:
            if key not in request:
                raise Exception("'"+key+"' must be provided")  
        request["studyID"] = self.id()
        rp = self._eLABJournalObject__api._request("/api/v1/experiments", "post", request)
        try:
            experimentID = int(rp)
            if experimentID>0:
                return(self._eLABJournalObject__api.experiment(experimentID))
            else:
                raise Exception("couldn't create experiment")  
        except:
            print(rp)
            raise Exception("couldn't create experiment")   
            