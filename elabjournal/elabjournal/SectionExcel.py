from .Section import * 

class SectionExcel(Section):

    def __init__(self, api, data):        
        """
        Internal use only: initialize section object
        """
        if (not(data==None) & (type(data) == dict) & 
            ("sectionType" in data.keys()) 
           ):
             if data["sectionType"]=="EXCEL":
                 super().__init__(api, data)
             else:   
                 raise Exception("no excel")                                         
        else:
            raise Exception("no (valid) section data") 
            
    def show(self):
        """
        Show the content
        """
        rp = self._eLABJournalObject__api._request("/api/v1/experiments/sections/"+urllib.parse.quote(str(self.id()))+"/excel/preview", "get", {}, stream=True)
        htmlCode = "<div style=\"border: 1px solid #067172; padding: 10px;\">"
        try:
            stream = BytesIO(rp.content)
            image = Image.open(stream)            
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img = base64.b64encode(buffered.getvalue()).decode("ascii")
            htmlCode = htmlCode+"<figure style=\"display: inline-block; margin-right: 10px; margin-bottom: 10px;\">"
            htmlCode = htmlCode+"<img src=\"data:image/jpeg;base64,"+format(img)+"\">"
            htmlCode = htmlCode+"</figure>"            
        except:
            htmlCode = htmlCode+"<b>No preview available for Excel content</b>"  
        htmlCode = htmlCode + "</div>"                                                    
        return(HTML(htmlCode))       
            
    def get(self):
        """
        Get the content of this section
        """ 
        rp = self._eLABJournalObject__api._request("/api/v1/experiments/sections/"+urllib.parse.quote(str(self.id()))+"/excel", "get", {}, stream=True)
        wb = openpyxl.load_workbook(BytesIO(rp.content))
        return(wb)
            
    def set(self, data):
        """
        Set or update the content of this section
        """ 
        if type(data) == openpyxl.workbook.workbook.Workbook:
            location = "/api/v1/experiments/sections/"+urllib.parse.quote(str(self.id()))+"/excel"
            rp = self._eLABJournalObject__api._request(location, "put", openpyxl.writer.excel.save_virtual_workbook(data), headers={"Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})                
        else:
            raise Exception("data type not supported for "+self.type()) 
                    