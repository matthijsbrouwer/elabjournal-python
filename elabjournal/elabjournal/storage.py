from .pager import *
import json
import pandas as pd
import urllib.parse

class storage:

    def __init__(self, api, data):
        """
        Internal use only: initialize storage object
        """
        if ((data is not None) & (type(data) == dict) & 
            ("storageID" in data) & 
            ("name" in data)
           ):
            self.__api = api
            self.__storageID = data["storageID"]
            self.__name = data["name"]
            self.__title = "Storage '"+self.__name+"' ("+str(self.__storageID)+")"
            self.__data = data
        else:
            raise Exception("no (valid) storage data") 
        
    def __repr__(self):
        """
        Internal use only: description storage object
        """ 
        return(self.__title)
        
    def name(self):
        """
        Get the name of the storage.
        """
        return(self.__name)
        
    def id(self):
        """
        Get the id of the storage.
        """
        return(self.__storageID)    
        
    def barcode(self):
        """
        Get the barcode of the storage (layer).
        """
        if "barcode" in self.__data:
            barcode = self.__data["barcode"]
            return(barcode)
        return None
        
    def storage_layer(self):
        """
        Get the storage layer.
        """
        if "storageLayerID" in self.__data:
            storageLayerID = self.__data["storageLayerID"]
            if storageLayerID>0:
                return(self.__api.storage_layer(storageLayerID))
        return None     
        
    def data(self):
        """
        Get the data describing the storage.
        """
        return(self.__data)   
        
    def statistics(self):
        """
        Get statistics for storage .
        """
        request = {} 
        rp = self.__api.request("/api/v1/storage/"+urllib.parse.quote(str(self.__storageID))+"/statistics", "get", request) 
        #check and get
        if (rp is not None) & (type(rp) == dict):
            return(rp)                                                 
        else:
            return(None)                           
        
    def samples(self, *args, **kwargs):
        """
        Get object to access samples for storage.
        
        Parameters (object)
        ----------------------
        class: parser
            Pass the result of the first() method on this object instead
        class: sample_type
            Filter by sampleTypeID of this object 
        
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
            separate values with comma for multiple expands
            location, quantity, meta, experiments
        sort : str, optional    
            Sort by a specific field
        checkedOut : str, optional
            Filter for checked out samples
        minimumQuantityAmount : str, optional
            Filter for samples that have a minimum quantity amount set
        name : str, optional
            Filter by sample name
        sampleTypeID : str, optional
            Filter by sampleTypeID  
        barcodes : str, optional
            Filter by barcodes (comma-separated)
        search : str, optional
            Search term to use for filtering samples. 
        quantityID : str, optional
            Filter by quantityID
        """    
        request = {}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["checkedOut", "name", "sampleTypeID", "barcodes", 
                       "search", "quantityID"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if type(check_arg)==pager:
                    check_arg = arg.first(True)
                if type(check_arg)==sample_type:
                    request["sampleTypeID"] = check_arg.id()
                else:
                    raise Exception("unsupported object '"+str(type(check_arg))+"'")                 
        if kwargs is not None:
            for key, value in kwargs.items():
                if key in kwargs_special:
                    request["$"+key] = value   
                elif key in kwargs_keys:
                    request[key] = value
                else:
                    raise Exception("unsupported key '"+key+"'")   
        return(pager(self.__api, "Samples", "/api/v1/storage/"+urllib.parse.quote(str(self.__storageID))+"/samples", request, "sampleID", 5, self.__api.sample))
          
     
    