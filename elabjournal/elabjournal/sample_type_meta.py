from .pager import *
import json
import pandas as pd

class sample_type_meta:

    def __init__(self, api, data):        
        if ((data is not None) & (type(data) == dict) & 
            ("sampleTypeMetaID" in data.keys()) & 
            ("key" in data.keys())
           ):
            self.__api = api
            self.__sampleTypeMetaID = data["sampleTypeMetaID"]
            self.__key = data["key"]
            self.__title = "Sample type meta '"+self.__key+"' ("+str(self.__sampleTypeMetaID)+")"
            self.__data = data
        else:
            raise Exception("no (valid) sampleTypeMeta data") 
        
    def __repr__(self):
        return(self.__title)
        
    def key(self):
        return(self.__key)
        
    def id(self):
        return(self.__sampleTypeMetaID)    
        
    def data(self):
        return(self.__data)   
           
    