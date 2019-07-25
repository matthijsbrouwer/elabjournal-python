import json
import pandas as pd

class sample_type:

    def __init__(self, api, data):        
        if ((data is not None) & (type(data) == dict) & 
            ("sampleTypeID" in data.keys()) & 
            ("name" in data.keys())
           ):
            self.__api = api
            self.__sampleTypeID = data["sampleTypeID"]
            self.__name = data["name"]
            self.__title = "Sample type '"+self.__name+"' ("+str(self.__sampleTypeID)+")"
            self.__data = data
        else:
            raise Exception("no (valid) sampleType data") 
        
    def __repr__(self):
        return(self.__title)
        
    def name(self):
        """
        Get the name of the sample type.
        """
        return(self.__name)
        
    def id(self):
        """
        Get the id of the sample serie.
        """
        return(self.__sampleTypeID)    
        
    def data(self):
        """
        Get the data describing the sample type.
        """
        return(self.__data)   
        
    def metas(self):
        return self.__api.sample_type_metas(self.__sampleTypeID)               
    
    