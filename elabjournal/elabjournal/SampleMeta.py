from .eLABJournalObject import * 

class SampleMeta(eLABJournalObject):

    def __init__(self, api, data):        
        if ((data is not None) & (type(data) == dict) & 
            ("sampleTypeMetaID" in data.keys()) & 
            ("key" in data.keys()) & 
            ("value" in data.keys())
           ):
            self.__key = data["key"]
            self.__value = data["value"]
            self.__sampleTypeMetaID = data["sampleTypeMetaID"]
            super().__init__(api, data, "sampleMetaID", str(data["key"])) 
        else:
            raise Exception("no (valid) sampleTypeMeta data") 
        
    
    def key(self):
        """
        Get key.
        """
        return(self.__key)
        
    def value(self):
        """
        Get value.
        """
        return(self.__value)               