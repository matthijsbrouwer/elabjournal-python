import json
import pandas as pd

class study:

    def __init__(self, api, data):
        """
        Internal use only: initialize study object
        """
        if ((data is not None) & (type(data) == dict) & 
            ("studyID" in data) & 
            ("name" in data)
           ):
            self.__api = api
            self.__studyID = data["studyID"]
            self.__name = data["name"]
            self.__title = "Study '"+self.__name+"' ("+str(self.__studyID)+")"
            self.__data = data
        else:
            raise Exception("no (valid) study data") 
        
    def __repr__(self):
        """
        Internal use only: description study object
        """ 
        return(self.__title)
        
    def name(self):
        """
        Get the name of the study.
        """
        return(self.__name)
        
    def id(self):
        """
        Get the id of the study.
        """
        return(self.__studyID)    
        
    def data(self):
        """
        Get the data describing the study.
        """
        return(self.__data)   
        
      