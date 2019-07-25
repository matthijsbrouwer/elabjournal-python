from .pager import *
import pandas as pd
import matplotlib
import urllib.parse

class experiment:

    def __init__(self, api, data):        
        """
        Internal use only: initialize experiment object
        """
        if ((data is not None) & (type(data) == dict) & 
            ("experimentID" in data.keys()) &
            ("name" in data.keys())
           ):
            self.__api = api
            self.__experimentID = data["experimentID"]
            self.__name = data["name"]
            self.__title = "Experiment '"+self.__name+"' ("+str(self.__experimentID)+")"
            self.__data = data
        else:
            raise Exception("no (valid) experiment data") 
        
    def __repr__(self):
        """
        Internal use only: description experiment object
        """ 
        return(self.__title)
            
    def name(self):
        """
        Get the name of the experiment.
        """
        return(self.__name)
        
    def id(self):
        """
        Get the id of the experiment.
        """
        return(self.__experimentID)
        
    def data(self):
        """
        Get the data describing the experiment.
        """
        return(self.__data)   
        
    def sections(self, *args, **kwargs):
        """
        Get object to access projects.
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
        sort : str, optional    
            Sort by a specific field
        archived : str, optional
            Filter by archived or non-archived sections.
        """    
        request = {"$sort": "order"}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["archived"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if type(check_arg)==pager:
                    check_arg = arg.first(True)
                raise Exception("unsupported object '"+str(type(check_arg))+"'")                 
        if kwargs is not None:
            for key, value in kwargs.items():
                if key in kwargs_special:
                    request["$"+key] = value   
                elif key in kwargs_keys:
                    request[key] = value
                else:
                    raise Exception("unsupported key '"+key+"'")             
        return(pager(self.__api,"Experiment Sections", 
                     "/api/v1/experiments/"+urllib.parse.quote(str(self.__experimentID))+"/sections", request, "expJournalID", 5, self.section))
        
        
    def section(self, id):
        """
        Get section object with provided id (integer or string) belonging to this experiment.
        """ 
        request = {}
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            section = self.__api.section(id)        
            if section is not None:
                #check experimentID
                if section.data()["experimentID"]==self.__experimentID:
                    return(section)
            return None
        else:
            raise Exception("incorrect call")    
    
    def add(self, data, title=None, order=None):
        if data is None:
            return(None)
        elif type(data) == section:
            sectionType = data.type()
            if title==None:
                sectionHeader = data.title()
            else:
                sectionHeader = title
            sectionData = data.get()    
        else:
            if title==None:
                sectionHeader = "New section"
            else:
                sectionHeader = title
            if type(data) == pd.DataFrame:
                sectionType = "DATATABLE"
                sectionData = data
            elif type(data) == matplotlib.figure.Figure:    
                sectionType = "CANVAS"
                sectionData = data
            elif type(data) == PngImagePlugin.PngImageFile:   
                sectionType = "CANVAS"
                sectionData = data
            else:
                raise Exception("no (valid) section data")
        #create new section    
        request = {"sectionType": sectionType, "sectionHeader": sectionHeader}
        location = "/api/v1/experiments/"+urllib.parse.quote(str(self.__experimentID))+"/sections"
        section_id = self.__api.request(location, "post", json.dumps(request))       
        #get new section
        new_section = self.__api.section(section_id)
        #put content in section
        new_section.set(sectionData)
        #return new section
        return(new_section)
        
            
            
        
        