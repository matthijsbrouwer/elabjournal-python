from .pager import *
from .section import *
import pandas as pd
import matplotlib

class experiment:

    def __init__(self, api, data):        
        if (not(data==None) & (type(data) == dict) & 
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
        return(self.__title)
        
    
    def sections(self, search=None):
        request = {}
        if not(search==None):
            request["search"] = search
        return(pager(self.__api,"Experiment Sections", 
                     "/api/v1/experiments/"+str(self.__experimentID)+"/sections", request, "expJournalID", "order", 5))
        
        
    def section(self, section_id):
        return(self.__api.section(section_id))
    
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
        location = "/api/v1/experiments/"+str(self.__experimentID)+"/sections"
        section_id = self.__api.request(location, "post", json.dumps(request))       
        #get new section
        new_section = self.__api.section(section_id)
        #put content in section
        new_section.set(sectionData)
        #return new section
        return(new_section)
        
            
            
        
        