import json
import pandas as pd

class sample_meta:

    def __init__(self, api, data):        
        if ((data is not None) & (type(data) == dict) & 
            ("sampleMetaID" in data.keys()) & 
            ("sampleTypeMetaID" in data.keys()) & 
            ("key" in data.keys()) & 
            ("value" in data.keys())
           ):
            self.__api = api
            self.__sampleMetaID = data["sampleMetaID"]
            self.__sampleTypeMetaID = data["sampleTypeMetaID"]
            self.__key = data["key"]
            self.__title = "Sample meta '"+self.__key+"' ("+str(self.__sampleMetaID)+")"
            self.__data = data
        else:
            raise Exception("no (valid) sampleTypeMeta data") 
        
    def __repr__(self):
        return(self.__title)
        
    def key(self):
        return(self.__key)
        
    def id(self):
        return(self.__sampleMetaID)    
        
    def sampleType(self):
        return self.__api.sample_type(self.__sampleTypeID)        
        
    def data(self):
        return(self.__data)   
           
    