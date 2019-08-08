from .eLABJournalObject import *

class SampleTypeMeta(eLABJournalObject):

    def __init__(self, api, data):        
        if ((data is not None) & (type(data) == dict) & 
            ("key" in data.keys()) 
           ):
            self.__key = data["key"]
            super().__init__(api, data, "sampleTypeMetaID", str(data["key"])) 
        else:
            raise Exception("no (valid) sampleTypeMeta data") 
        
    def key(self):
        """
        Get key.
        """
        return(self.__key)
        
    def visualize(self):
        """
        Show visualization.
        """
        sample_type = self.sample_type()
                     
        g = super().visualize()
        
        if sample_type:
            sample_type_id = str(sample_type.id())
            sample_type_name = str(sample_type.name()) 
            with g.subgraph(name="cluster_sampletype") as g_sampletype:
                g_sampletype.attr(tooltip="sample type", label="sampleTypeID "+sample_type_id, style="filled", color="black", fillcolor="#EEEEEE")
                g_sampletype.node("sample_type",sample_type_name, {"tooltip": "type of sample", "style": "filled", "fillcolor": "white", "shape": "rect"})
            g.edge("sample_type", "class_name",None,{"constraint" : "false"})
        
        return(g)      
            
    def sample_type(self):
        """
        Get the sample type as an object.
        """
        data = self.data()
        if "sampleTypeID" in data.keys():
            sample_type_id = data["sampleTypeID"]
            if (sample_type_id is not None) and (sample_type_id is not 0):
                return self._eLABJournalObject__api.sample_type(sample_type_id)   
        return None           
        
                     
        
    
        
        
    