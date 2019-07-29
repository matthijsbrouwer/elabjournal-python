from .pager import *
import json
import pandas as pd
import urllib.parse

class storage_layer:

    def __init__(self, api, data):
        """
        Internal use only: initialize storage object
        """
        if ((data is not None) & (type(data) == dict) & 
            ("storageLayerID" in data) & 
            ("name" in data)
           ):
            self.__api = api
            self.__storageLayerID = data["storageLayerID"]
            self.__name = data["name"]
            self.__title = "Storage layer '"+self.__name+"' ("+str(self.__storageLayerID)+")"
            self.__data = data
        else:
            raise Exception("no (valid) storage layer data") 
        
    def __repr__(self):
        """
        Internal use only: description storage layer object
        """ 
        return(self.__title)
        
    def name(self):
        """
        Get the name of the storage layer.
        """
        return(self.__name)
        
    def id(self):
        """
        Get the id of the storage layer.
        """
        return(self.__storageLayerID)   
        
    def parent(self):
        """
        Get the parent storage layer.
        """
        if "parentStorageLayerID" in self.__data:
            parentStorageLayerID = self.__data["parentStorageLayerID"]
            if parentStorageLayerID>0:
                return(self.__api.storage_layer(parentStorageLayerID))
        return None     
        
    def barcode(self):
        """
        Get the barcode of the storage layer.
        """
        if "barcode" in self.__data:
            barcode = self.__data["barcode"]
            return(barcode)
        return None
        
    def data(self):
        """
        Get the data describing the storage layer.
        """
        return(self.__data)   
        
     