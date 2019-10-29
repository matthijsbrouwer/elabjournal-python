from .eLABJournalObject import * 

class SampleType(eLABJournalObject):

    def __init__(self, api, data):        
        if ((data is not None) & (type(data) == dict) & 
            ("name" in data.keys())
           ):
            super().__init__(api, data, "sampleTypeID", str(data["name"]))                        
        else:
            raise Exception("no (valid) SampleType data") 
        
    def metas(self):
        """
        Get all the meta items (metas) for the sample type.
        """
        return self._eLABJournalObject__api.sample_type_metas(self.id())               
    
    def meta(self, sample_type_meta_id):
        """
        Get sample type meta object with provided sample_type_meta_id.
        """
        return self._eLABJournalObject__api.sample_type_meta(self.id(), sample_type_meta_id)               
    
    def visualize(self):
        """
        Create visualization.
        """
        g = super().visualize()
        
        metas = self.metas().all()
        if len(metas)>0:
            with g.subgraph(name="cluster_metas") as g_metas:
                htmlCode = "<<table bgcolor=\"#FFFFFF\" border=\"0\" cellborder=\"1\" cellspacing=\"0\">"
                htmlCode = htmlCode + "<tr><td><b>name</b></td><td><b>type</b></td><td><b>required</b></td></tr>"
                for metaID in metas.index:
                    meta_name = str(metas.loc[metaID]["key"])
                    meta_type = str(metas.loc[metaID]["sampleDataType"])
                    meta_required = str(metas.loc[metaID]["required"])
                    htmlCode = htmlCode + "<tr><td>"+html.escape(meta_name)+"</td><td>"+html.escape(meta_type)+"</td><td>"+html.escape(meta_required)+"</td></tr>"                
                htmlCode = htmlCode + "</table>>"
                g_metas.attr(labelloc="b", label=htmlCode, style="filled", color="black", fillcolor="#EEEEEE")                                          
                g_metas.node("metas","Sample Type Metas",{"shape": "rect", "style": "filled", "fillcolor": "white"})                                    
            g.edge("class_name","metas",None,{}) 
        
        return(g) 
        
    