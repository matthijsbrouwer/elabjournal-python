from .Section import * 



class SectionCanvas(Section):

    def __init__(self, api, data):        
        """
        Internal use only: initialize section object
        """
        if (not(data==None) & (type(data) == dict) & 
            ("sectionType" in data.keys()) 
           ):
             if data["sectionType"]=="CANVAS":
                 super().__init__(api, data)
             else:   
                 raise Exception("no canvas")                                         
        else:
            raise Exception("no (valid) section data") 
            
    def show(self):
        """
        Show the content
        """
        image = self.get()
        htmlCode = "<div style=\"border: 1px solid #067172; padding: 10px;\">"
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img = base64.b64encode(buffered.getvalue()).decode("ascii")
        htmlCode = htmlCode+"<figure style=\"display: inline-block; margin-right: 10px; margin-bottom: 10px;\">"
        htmlCode = htmlCode+"<img src=\"data:image/jpeg;base64,"+format(img)+"\">"
        htmlCode = htmlCode+"</figure>"
        htmlCode = htmlCode + "</div>"                                                    
        return(HTML(htmlCode))  
            
    def get(self):
        """
        Get the content of this section
        """ 
        rp = self._eLABJournalObject__api._request("/api/v1/experiments/sections/"+urllib.parse.quote(str(self.id()))+"/canvas", "get", {}, stream=True)
        stream = BytesIO(rp.content)
        return(Image.open(stream))                                                    
            
    def set(self, data):
        """
        Set or update the content of this section
        """ 
        location = "/api/v1/experiments/sections/"+urllib.parse.quote(str(self.id()))+"/canvas"
        if type(data) == matplotlib.figure.Figure:
            sizes = data.get_size_inches()
            dpi = 825/sizes[0]
            figfile = BytesIO()
            data.savefig(figfile, format="png", dpi=dpi, bbox_inches="tight")
            rp = self._eLABJournalObject__api._request(location, "put", figfile.getvalue(), headers={"Content-Type": "image/png"}) 
        elif type(data) == PngImagePlugin.PngImageFile:
            with BytesIO() as output:
                data.save(output, format="png")
                contents = output.getvalue()
            rp = self._eLABJournalObject__api._request(location, "put", contents, headers={"Content-Type": "image/png"}) 
        else:
            raise Exception("data type not supported to set "+self.__sectionType) 
                    