import json
import pandas as pd
import numbers

class sample_serie:

    def __init__(self, api, data):        
        """
        Internal use only: initialize sample serie
        """
        if ((data is not None) & (type(data) == dict) & 
            ("seriesID" in data.keys()) & 
            ("name" in data.keys())
           ):
            self.__api = api
            self.__seriesID = data["seriesID"]
            self.__name = data["name"]
            self.__title = "Sample serie '"+self.__name+"' ("+str(self.__seriesID)+")"
            self.__data = data
        else:
            raise Exception("no (valid) sampleSerie data") 
        
    def __repr__(self):
        """
        Internal use only: description sample serie object
        """ 
        return(self.__title)
        
    def name(self):
        """
        Get the name of the sample serie.
        """
        return(self.__name)
        
    def id(self):
        """
        Get the id of the sample serie.
        """
        return(self.__seriesID)    
        
    def barcode(self):
        """
        Get the barcode of the sample.
        """
        if "barcode" in self.__data:
            barcode = self.__data["barcode"]
            return(barcode)
        return None
        
    def data(self):
        """
        Get the data describing the sample serie.
        """
        return({k:self.__data[k] for k in self.__data if k!="samples"})    
        
    def samples(self):
        """
        Get a dict with the samples for this sample serie.
        The sampleID is used as a key, the value is a sample object.
        """
        result = {}
        if "samples" in self.__data:
            samplesData = self.__data["samples"]
            if isinstance(samplesData, list):
                for sampleItem in samplesData:
                    if isinstance(sampleItem,dict) & ("sampleID" in sampleItem):
                        result[sampleItem["sampleID"]] = self.__api.sample(sampleItem["sampleID"])
                    elif isinstance(sampleItem,numbers.Integral) | isinstance(sampleItem,str):
                        result[sampleItem] = self.__api.sample(sampleItem)                             
        return result               
    
    