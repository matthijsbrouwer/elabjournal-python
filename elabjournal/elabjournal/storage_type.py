from .pager import *
import json
import pandas as pd
import urllib.parse

class storage_type:

    def __init__(self, api, data):
        """
        Internal use only: initialize storage object
        """
        if ((data is not None) & (type(data) == dict) & 
            ("storageTypeID" in data) & 
            ("name" in data)
           ):
            self.__api = api
            self.__storageTypeID = data["storageTypeID"]
            self.__name = data["name"]
            self.__title = "Storage type '"+self.__name+"' ("+str(self.__storageTypeID)+")"
            self.__data = data
        else:
            raise Exception("no (valid) storage type data") 
        
    def __repr__(self):
        """
        Internal use only: description storage type object
        """ 
        return(self.__title)
        
    def name(self):
        """
        Get the name of the storage type.
        """
        return(self.__name)
        
    def id(self):
        """
        Get the id of the storage type.
        """
        return(self.__storageTypeID)    
        
    def data(self):
        """
        Get the data describing the storage type.
        """
        return(self.__data)   
        
     