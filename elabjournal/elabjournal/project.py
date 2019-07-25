import json
import pandas as pd

class project:

    def __init__(self, api, data):
        """
        Internal use only: initialize project object
        """
        if ((data is not None) & (type(data) == dict) & 
            ("projectID" in data) & 
            ("name" in data)
           ):
            self.__api = api
            self.__projectID = data["projectID"]
            self.__name = data["name"]
            self.__title = "project '"+self.__name+"' ("+str(self.__projectID)+")"
            self.__data = data
        else:
            raise Exception("no (valid) project data") 
        
    def __repr__(self):
        """
        Internal use only: description project object
        """ 
        return(self.__title)
        
    def name(self):
        """
        Get the name of the project.
        """
        return(self.__name)
        
    def id(self):
        """
        Get the id of the project.
        """
        return(self.__projectID)    
        
    def data(self):
        """
        Get the data describing the project.
        """
        return(self.__data)   
        
      