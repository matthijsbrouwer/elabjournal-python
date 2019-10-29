from .eLABJournalObject import * 

import urllib.parse

class SampleMeta(eLABJournalObject):

    def __init__(self, api, sample_id, data):        
        if ((data is not None) & (sample_id is not None) & (type(data) == dict) & 
            ("sampleTypeMetaID" in data.keys()) & 
            ("key" in data.keys()) 
           ):
            self.__key = data["key"]
            if "value" in data.keys():
                self.__value = data["value"]
            else:
                self.__value = None    
            self.__sampleID = sample_id
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
        
    def update(self, *args, **kwargs):
        """
        Update the meta.
        
        See update_sample_meta on the api for the available/allowed parameters       
        
        """    
        kwargs["sampleID"] = self.__sampleID
        kwargs["sampleMetaID"] = self.id()
        self._eLABJournalObject__api.update_sample_meta(*list(args), **dict(kwargs))
        rp = self._eLABJournalObject__api._request("/api/v1/samples/"+urllib.parse.quote(str(kwargs["sampleID"]))+"/meta/"+urllib.parse.quote(str(kwargs["sampleMetaID"])), "get", {})
        #check and get
        if (rp is not None) & (type(rp) == dict):
            self.__init__(self._eLABJournalObject__api,kwargs["sampleID"],rp)                                               
        else:
            print(dict)
            raise Exception("couldn't perform selfupdate")              