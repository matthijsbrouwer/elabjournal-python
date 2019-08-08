from .Section import * 

import pandas as pd

class SectionDatatable(Section):

    def __init__(self, api, data):        
        """
        Internal use only: initialize section object
        """
        if (not(data==None) & (type(data) == dict) & 
            ("sectionType" in data.keys()) 
           ):
             if data["sectionType"]=="DATATABLE":
                 super().__init__(api, data)
             else:   
                 raise Exception("no datatable")                                         
        else:
            raise Exception("no (valid) section data") 
            
    def show(self):
        """
        Show the content
        """
        datatable = self.get()
        htmlCode = "<div style=\"border: 1px solid #067172; padding: 10px;\">"+datatable.to_html(index=False, header=False)+"</div>"            
        return(HTML(htmlCode)) 
            
    def get(self):
        """
        Get the content of this section
        """ 
        rp = self._eLABJournalObject__api._request("/api/v1/experiments/sections/"+urllib.parse.quote(str(self.id()))+"/datatable", "get", {})
        if not(rp==None) & (type(rp) == list):
            return(pd.DataFrame(rp))                                                 
        else:
            raise Exception("section type "+self.__sectionType+" returns unexpected data")
            
    def set(self, data):
        """
        Set or update the content of this section
        """ 
        if type(data) == pd.DataFrame:
            location = "/api/v1/experiments/sections/"+urllib.parse.quote(str(self.id()))+"/datatable"
            rp = self._eLABJournalObject__api._request(location, "put", json.dumps(data.values.tolist()), headers={"Content-Type": "application/json"})                
        else:
            raise Exception("data type not supported to set "+self.__sectionType) 
                    