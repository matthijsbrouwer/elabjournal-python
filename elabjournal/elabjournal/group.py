import json
import pandas as pd
import numbers

class group:

    def __init__(self, api, data):        
        """
        Internal use only: initialize sample serie.
        """
        if ((data is not None) & (type(data) == dict) & 
            ("groupID" in data.keys()) & 
            ("name" in data.keys())
           ):
            self.__api = api
            self.__groupID = data["groupID"]
            self.__name = data["name"]
            self.__title = "Group '"+self.__name+"' ("+str(self.__groupID)+")"
            self.__data = data
        else:
            raise Exception("no (valid) group data") 
        
    def __repr__(self):
        """
        Internal use only: description group object.
        """ 
        return(self.__title)
        
    def name(self):
        """
        Get the name of the group.
        """
        return(self.__name)
        
    def id(self):
        """
        Get the id of the group.
        """
        return(self.__groupID)    
        
    def data(self):
        """
        Get the data describing the group.
        """
        return(self.__data)    
        
    