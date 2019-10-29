from .eLABJournalObject import * 
import urllib.parse
import html

class Sample(eLABJournalObject):

    def __init__(self, api, data):  
        """
        Internal use only: initialize sample object
        """
        if ((data is not None) & (type(data) == dict) & 
            ("name" in data.keys())
           ):
            super().__init__(api, data, "sampleID", str(data["name"]))            
            if ("sampleType" in data.keys()) & (type(data["sampleType"]) == dict) & ("sampleTypeID" in data["sampleType"]):
                self.__sampleTypeID = data["sampleType"]["sampleTypeID"]
            else:
                self.__sampleTypeID = None
            if "seriesID" in data.keys():
                self.__seriesID = data["seriesID"]
            else:
                self.__seriesID = None     
            if "storageLayerID" in data.keys():
                self.__storageLayerID = data["storageLayerID"]
            else:
                self.__storageLayerID = None                               
        else:
            raise Exception("no (valid) Sample data") 
        
    def visualize(self):
        """
        Show visualization.
        """
        sample_id = str(self.id())
        sample_name = str(self.name()) 
        sample_type = self.sample_type()
        sample_serie = self.sample_serie()
                     
        storage_layer = self.storage_layer()
        storage = self.storage()        
        
        g = graphviz.Digraph()
        
        with g.subgraph(name="cluster_sample") as g_sample:
            g_sample.attr(tooltip="sample", label="expJournalID "+sample_id, style="filled", color="black", fillcolor="#067172", fontcolor="white")
            g_sample.node("sample_name",sample_name, {"tooltip": "title of sample", "style": "filled", "color": "#0B3B52", "fontcolor": "white", "shape": "rect"})                        
        
        if sample_serie:
            sample_serie_id = str(sample_serie.id())
            sample_serie_name = str(sample_serie.name()) 
            with g.subgraph(name="cluster_sampleserie") as g_sampleserie:
                g_sampleserie.attr(tooltip="sample type", label="serieID "+sample_serie_id, style="filled", color="black", fillcolor="#EEEEEE")
                g_sampleserie.node("sample_serie",sample_serie_name, {"tooltip": "type of sample", "style": "filled", "fillcolor": "white", "shape": "rect"})
            g.edge("sample_serie","sample_name",None,{"rank": "source"})   
                                            
        if sample_type:
            sample_type_id = str(sample_type.id())
            sample_type_name = str(sample_type.name()) 
            with g.subgraph(name="cluster_sampletype") as g_sampletype:
                g_sampletype.attr(tooltip="sample type", label="sampleTypeID "+sample_type_id, style="filled", color="black", fillcolor="#EEEEEE")
                g_sampletype.node("sample_type",sample_type_name, {"tooltip": "type of sample", "style": "filled", "fillcolor": "white", "shape": "rect"})
            g.edge("sample_name","sample_type",None,{})   
                                            
        if storage_layer:
            storage_layer_id = str(storage_layer.id())
            storage_layer_name = str(storage_layer.name()) 
            with g.subgraph(name="cluster_storage_layer") as g_storage_layer:
                g_storage_layer.attr(tooltip="storage_layer", label="storage_layerID "+storage_layer_id, style="filled", color="black", fillcolor="#EEEEEE")
                g_storage_layer.node("storage_layer_name",storage_layer_name, {"tooltip": "name of storage_layer", "style": "filled", "fillcolor": "white", "shape": "rect"})                        
            g.edge("storage_layer_name","sample_name",None,{"constraint": "false"})          
            if storage:
                storage_id = str(storage.id())
                storage_name = str(storage.name())
                with g.subgraph(name="cluster_storage") as g_storage:
                    g_storage.attr(tooltip="storage", label="storageID "+storage_id, style="filled", color="black", fillcolor="#EEEEEE")
                    g_storage.node("storage_name",storage_name, {"tooltip": "name of storage_layer", "style": "filled", "fillcolor": "white", "shape": "rect"})   
                g.edge("storage_name","storage_layer_name",None,{"constraint": "false"})  
                       
        metas = self.metas().all()
        if len(metas)>0:
            with g.subgraph(name="cluster_metas") as g_metas:
                htmlCode = "<<table bgcolor=\"#FFFFFF\" border=\"0\" cellborder=\"1\" cellspacing=\"0\">"
                htmlCode = htmlCode + "<tr><td><b>name</b></td><td><b>type</b></td><td><b>value</b></td></tr>"
                for metaID in metas.index:
                    meta_name = str(metas.loc[metaID]["key"])
                    meta_type = str(metas.loc[metaID]["sampleDataType"])
                    meta_value = str(metas.loc[metaID]["value"])
                    htmlCode = htmlCode + "<tr><td>"+html.escape(meta_name)+"</td><td>"+html.escape(meta_type)+"</td><td>"+html.escape(meta_value)+"</td></tr>"                
                htmlCode = htmlCode + "</table>>"
                g_metas.attr(labelloc="b", label=htmlCode, style="filled", color="black", fillcolor="#EEEEEE")                                          
                g_metas.node("metas","Sample Metas",{"shape": "rect", "style": "filled", "fillcolor": "white"})                                    
            if storage_layer:
                g.edge("storage_layer_name","metas",None,{"rank": "source", "style": "invis"})
                if storage:
                    g.edge("storage_name","metas",None,{"rank": "source", "style": "invis"})
            g.edge("sample_name","metas",None,{})            
                                  
        return(g)  
        
    def barcode(self):
        """
        Get the barcode of the sample.
        """
        if "barcode" in self.data():
            barcode = self.data()["barcode"]
            return(barcode)
        return None
        
    def sample_type(self):
        """
        Get the sample type of the sample as an object.
        """
        if (self.__sampleTypeID is not None) & (self.__sampleTypeID is not 0):
            return self._eLABJournalObject__api.sample_type(self.__sampleTypeID)   
        return None           
        
    def sample_serie(self):
        """
        Get the sample serie of the sample as an object.
        """
        if (self.__seriesID is not None) & (self.__seriesID is not 0):
            return self._eLABJournalObject__api.sample_serie(self.__seriesID) 
        return None               
        
    def storage_layer(self):
        """
        Get the storage layer of the sample as an object.
        """
        if (self.__storageLayerID is not None) & (self.__storageLayerID is not 0):
            return self._eLABJournalObject__api.storage_layer(self.__storageLayerID)                  
        return None      
        
    def storage(self):
        """
        Get the storage of the sample as an object.
        """
        storage_layer = self.storage_layer()
        if storage_layer is not None:
            return storage_layer.storage()   
        return None      
        
    def metas(self):
        """
        Get all the meta items (metas) for the sample.
        """
        return self._eLABJournalObject__api.sample_metas(self.id())    
        
    def meta(self, sample_meta_id):
        """
        Get meta item (meta) with provided sample_meta_id for the sample.
        """
        return self._eLABJournalObject__api.sample_meta(self.id(), sample_meta_id)  
        
    def update_meta(self, *args, **kwargs):
        """
        Update the meta.
        
        See update_sample_meta on the api for the available/allowed parameters  
        """
        kwargs["sampleID"] = self.id()
        return self._eLABJournalObject__api.update_sample_meta(*list(args), **dict(kwargs))
        
    def create_meta(self, *args, **kwargs):
        """
        Create meta.
        
        See create_sample_meta on the api for the available/allowed parameters  
        """
        kwargs["sampleID"] = self.id()
        return self._eLABJournalObject__api.create_sample_meta(*list(args), **dict(kwargs))
        
    def delete_meta(self, *args, **kwargs):
        """
        Delete meta.
        
        See delete_sample_meta on the api for the available/allowed parameters  
        """
        kwargs["sampleID"] = self.id()
        return self._eLABJournalObject__api.delete_sample_meta(self.id(), *list(args), **dict(kwargs))
        
    def update(self, *args, **kwargs):
        """
        Update the sample.
        
        See update_sample on the api for the available/allowed parameters       
        
        """   
        self._eLABJournalObject__api.update_sample(self.id(), *list(args), **dict(kwargs))
        rp = self._eLABJournalObject__api._request("/api/v1/samples/"+urllib.parse.quote(str(self.id())), "get", {})
        #check and get
        if (rp is not None) & (type(rp) == dict):
            self.__init__(self._eLABJournalObject__api,rp)                                               
        else:
            raise Exception("couldn't perform selfupdate")
                          
    