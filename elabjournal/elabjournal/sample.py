from .sample_type import *
import json
import pandas as pd

class sample:

    def __init__(self, api, data):  
        """
        Internal use only: initialize sample object
        """
        if ((data is not None) & (type(data) == dict) & 
            ("sampleID" in data.keys()) & 
            ("name" in data.keys())
           ):
            self.__api = api
            self.__sampleID = data["sampleID"]
            self.__name = data["name"]
            self.__title = "Sample '"+self.__name+"' ("+str(self.__sampleID)+")"
            if ("sampleType" in data.keys()) & (type(data["sampleType"]) == dict) & ("sampleTypeID" in data["sampleType"]):
                self.__sampleTypeID = data["sampleType"]["sampleTypeID"]
            else:
                self.__sampleTypeID = None
            if "seriesID" in data.keys():
                self.__seriesID = data["seriesID"]
            else:
                self.__seriesID = None                    
            self.__data = data
        else:
            raise Exception("no (valid) sample data") 
        
    def __repr__(self):
        """
        Internal use only: description sample object
        """ 
        return(self.__title)
        
    def name(self):
        """
        Get the name of the sample.
        """
        return(self.__name)
        
    def id(self):
        """
        Get the id of the sample.
        """
        return(self.__sampleID)
        
    def barcode(self):
        """
        Get the barcode of the sample.
        """
        if "barcode" in self.__data:
            barcode = self.__data["barcode"]
            return(barcode)
        return None
        
    def sample_type(self):
        """
        Get the sampleType of the sample as an object.
        """
        return self.__api.sample_type(self.__sampleTypeID)        
        
    def sample_serie(self):
        """
        Get the sampleSerie of the sample as an object.
        """
        if "seriesID" in self.__data:
            return self.__api.sample_serie(self.__data["seriesID"]) 
        return None               
        
    def data(self):
        """
        Get the data describing the sample.
        """
        return(self.__data)   
        
    def metas(self):
        """
        Get all the meta items (metas) for the sample.
        """
        return self.__api.sample_metas(self.__sampleID)    
        
    def meta(self, sample_meta_id):
        """
        Get meta item (meta) with provided sample_meta_id for the sample.
        """
        return self.__api.sample_meta(self.__sampleID, sample_meta_id)             
    
    