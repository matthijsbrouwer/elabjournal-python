from .Section import * 


class SectionParagraph(Section):

    def __init__(self, api, data):        
        """
        Internal use only: initialize section object
        """
        if (not(data==None) & (type(data) == dict) & 
            ("sectionType" in data.keys()) 
           ):
             if data["sectionType"]=="PARAGRAPH":
                 super().__init__(api, data)
             else:   
                 raise Exception("no paragraph")                                         
        else:
            raise Exception("no (valid) section data") 
            
    def show(self):
        """
        Show the content
        """
        contents = self.get()["contents"]
        htmlCode = "<div style=\"border: 1px solid #067172; padding: 10px;\">"+contents+"</div>"
        return(HTML(htmlCode))
            
    def get(self):
        """
        Get the content of this section
        """ 
        rp = self._eLABJournalObject__api._request("/api/v1/experiments/sections/"+urllib.parse.quote(str(self.id()))+"/content", "get", {})
        if not(rp==None) & (type(rp) == dict):
            return(rp)                                                 
        else:
            raise Exception("section type "+self.__sectionType+" returns unexpected data")
            
        