from .Section import * 


class SectionSample(Section):

    def __init__(self, api, data):        
        """
        Internal use only: initialize section object
        """
        if (not(data==None) & (type(data) == dict) & 
            ("sectionType" in data.keys()) 
           ):
             if (data["sectionType"]=="SAMPLESIN") | (data["sectionType"]=="SAMPLESOUT"):
                 super().__init__(api, data)
             else:   
                 raise Exception("no samplesin or samplesout")                                         
        else:
            raise Exception("no (valid) section data") 
            
    def visualize(self):
        """
        Show visualization.
        """
        g = super().visualize()
        
        with g.subgraph(name="cluster_content") as g_content:
            samples = self.samples().all()
            for sampleID in samples.index:  
                sample_name = samples.loc[sampleID]["name"]
                with g_content.subgraph(name="cluster_sample_"+str(sampleID)) as g_sample:                                        
                    g_sample.attr(labelloc="b", tooltip="sample", label="sampleID "+str(sampleID), style="filled", color="black", fillcolor="#EEEEEE")
                    g_sample.node("sample_"+str(sampleID),sample_name,{"tooltip": "sample", "shape":"rect", "style": "filled", "fillcolor": "white"})
                g_content.edge("section_type","sample_"+str(sampleID),None,{}) 
        return(g)          
            
    def show(self):
        """
        Show the content.
        """
        samples = self.samples().all()
        htmlCode = "<div style=\"border: 1px solid #067172; padding: 10px;\">"
        for sampleID in samples.index:
            sample_name = str(samples.loc[sampleID]["name"])
            g = graphviz.Digraph()
            with g.subgraph(name="cluster_sample_"+str(sampleID)) as g_sample:
                g_sample.attr(label="sampleID "+str(sampleID), tooltip="sample", style="filled", color="black", fillcolor="#067172", fontcolor="white")
                g_sample.node("sample_name_"+str(sampleID),sample_name, {"tooltip": "sample", "style": "filled", "color": "#0B3B52", "fontcolor": "white", "shape": "rect"})                                
            htmlCode = htmlCode+"<figure style=\"display: inline-block; margin-right: 10px; margin-bottom: 10px;\">"
            htmlCode = htmlCode+g.pipe(format="svg").decode("utf-8")
            htmlCode = htmlCode+"</figure>"
        htmlCode = htmlCode + "</div>"                                                    
        return(HTML(htmlCode))  
            
    def samples(self, *args, **kwargs):
        """
        Get object to access metas.
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
        sort : str, optional    
            Sort by a specific field
        """    
        request = {}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = []
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg, eLABJournalPager):
                    check_arg = arg.first(True)
                raise Exception("unsupported object '"+str(type(check_arg))+"'")                 
        if kwargs is not None:
            for key, value in kwargs.items():
                if key in kwargs_special:
                    request["$"+key] = value   
                elif key in kwargs_keys:
                    request[key] = value
                else:
                    raise Exception("unsupported key '"+key+"'")             
        return(SectionMetas(self._eLABJournalObject__api,"Section samples", 
                     "/api/v1/experiments/sections/"+urllib.parse.quote(str(self.id()))+"/samples", request, "sampleID", 5, self._eLABJournalObject__api.sample))
        
     