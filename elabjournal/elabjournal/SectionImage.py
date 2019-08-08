from .Section import * 
from .ExperimentImages import * 

class SectionImage(Section):

    def __init__(self, api, data):        
        """
        Internal use only: initialize section object
        """
        if (not(data==None) & (type(data) == dict) & 
            ("sectionType" in data.keys()) 
           ):
             if data["sectionType"]=="IMAGE":
                 super().__init__(api, data)
             else:   
                 raise Exception("no image")                                         
        else:
            raise Exception("no (valid) section data") 
            
    def visualize(self):
        """
        Visualization
        """
        g = super().visualize()
        
        with g.subgraph(name="cluster_content") as g_content:
            images = self.get().all()
            for imageID in images.index:  
                image_description = images.loc[imageID]["description"] or images.loc[imageID]["realName"]
                image_name = images.loc[imageID]["realName"]
                with g_content.subgraph(name="cluster_image_"+str(imageID)) as g_image:                                        
                    g_image.attr(labelloc="b", tooltip=image_description, label="experimentimageID "+str(imageID), style="filled", color="black", fillcolor="#EEEEEE")
                    g_image.node("image_"+str(imageID),image_name,{"tooltip": image_description, "shape":"rect", "style": "filled", "fillcolor": "white"})
                g_content.edge("section_type","image_"+str(imageID),None,{})    
        
        return(g)        
            
    def show(self):
        """
        Show the content
        """
        images = self.get().all()
        htmlCode = "<div style=\"border: 1px solid #067172; padding: 10px;\">"
        for imageID in images.index:
            image_description = images.loc[imageID]["description"] or images.loc[imageID]["realName"]
            image_name = images.loc[imageID]["realName"]
            buffered = BytesIO()
            self.image(imageID,250).save(buffered, format="JPEG")
            img = base64.b64encode(buffered.getvalue()).decode("ascii")
            htmlCode = htmlCode+"<figure style=\"display: inline-block; margin-right: 10px; margin-bottom: 10px;\">"
            htmlCode = htmlCode+"<img title=\""+html.escape(image_description)+"\" src=\"data:image/jpeg;base64,"+format(img)+"\">"
            htmlCode = htmlCode+"<figcaption>"+html.escape(image_description)+"</figcaption>"
            htmlCode = htmlCode+"</figure>"
        htmlCode = htmlCode + "</div>"                                                    
        return(HTML(htmlCode))  
            
    def get(self):
        """
        Get the content of this section
        """ 
        return(ExperimentImages(self._eLABJournalObject__api, "Images", "/api/v1/experiments/sections/"+urllib.parse.quote(str(self.id()))+"/images", {}, "experimentFileID", 5, self.image))                                  
                                                         
            
    def image(self, id, *args, **kwargs):
        """
        Get image with the provided id (integer or string) for this section (only if section of type IMAGE).
        
        Parameters (key/value)
        ----------------------
        maxWidth : str, optional
            Maximum width image
        """
        if isinstance(id,numbers.Integral) | isinstance(id,str): 
            request = {}
            kwargs_special = []
            kwargs_keys = ["maxWidth"]
            if args is not None:
                for arg in args:
                    check_arg = arg                    
                    if isinstance(check_arg,numbers.Integral) | isinstance(check_arg,str):
                        request["maxWidth"] = str(check_arg)  
                    else:    
                        raise Exception("unsupported object '"+str(type(check_arg))+"'")                 
            if kwargs is not None:
                for key, value in kwargs.items():
                    if key in kwargs_special:
                        request["$"+key] = value   
                    elif key in kwargs_keys:
                        request[key] = value
                    else:
                        raise Exception("unsupported key '"+key+"'")             
        
            rp = self._eLABJournalObject__api._request("/api/v1/experiments/sections/"+urllib.parse.quote(str(self.id()))+"/images/"+urllib.parse.quote(str(id)), "get", request, stream=True)
            try:
                stream = BytesIO(rp.content)
                return(Image.open(stream))
            except:
                return(None)      
        else:
            raise Exception("incorrect call")                                                
     
                    
                    
                    
                    