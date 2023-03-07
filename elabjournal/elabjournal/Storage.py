from .eLABJournalObject import * 
from .Samples import *

import urllib.parse

class Storage(eLABJournalObject):

    def __init__(self, api, data):
        """
        Internal use only: initialize storage object
        """
        if ((data is not None) & (type(data) == dict) & 
            ("name" in data)
           ):
            super().__init__(api, data, "storageID", str(data["name"]))            
        else:
            raise Exception("no (valid) Storage data") 
            
    def visualize(self):
        """
        Create visualization.
        """
        g = super().visualize()
        
        storage_type = self.storage_type()
        
        if storage_type:
            storage_type_id = str(storage_type.id())
            storage_type_name = str(storage_type.name())
            storage_type_type = str(storage_type.type())
            with g.subgraph(name="cluster_type") as g_type:
                g_type.attr(tooltip="type of storage", label="storageTypeID "+storage_type_id, style="filled", color="black", fillcolor="#EEEEEE")
                g_type.node("storage_type_name",storage_type_name, {"tooltip": "type of storage", "style": "filled", "fillcolor": "white", "shape": "rect"})                                       
                g_type.node("storage_type_type",storage_type_type, {"tooltip": "type of storage", "style": "filled", "fillcolor": "white", "shape": "rect"})                                       
            g.edge("storage_type_type", "class_name", None, {"constraint": "false"})
            
        return(g)              
        
    def barcode(self):
        """
        Get the barcode of the storage (layer).
        """
        if "barcode" in self.data():
            barcode = self.data()["barcode"]
            return(barcode)
        return None
        
    def storage_layer(self):
        """
        Get the storage layer.
        """
        if "storageLayerID" in self.data():
            storageLayerID = self.data()["storageLayerID"]
            if storageLayerID>0:
                return(self._eLABJournalObject__api.storage_layer(storageLayerID))
        return None     
        
    def storage_type(self):
        """
        Get the storage type.
        """
        if "storageType" in self.data():
            storageType = self.data()["storageType"]
            if isinstance(storageType, dict) & ("storageTypeID" in storageType.keys()):
                storageTypeID = storageType["storageTypeID"]
                return(self._eLABJournalObject__api.storage_type(storageTypeID))
        return None     
        
    def statistics(self):
        """
        Get statistics for storage.
        """
        request = {} 
        rp = self._eLABJournalObject__api._request("/api/v1/storage/"+urllib.parse.quote(str(self.id()))+"/statistics", "get", request) 
        #check and get
        if (rp is not None) & (type(rp) == dict):
            return(rp)                                                 
        else:
            return(None)                           
        
    def samples(self, *args, **kwargs):
        """
        Get object to access samples for storage.
        
        Parameters (object)
        ----------------------
        class: parser
            Pass the result of the first() method on this object instead
        class: sample_type
            Filter by sampleTypeID of this object 
        
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
            separate values with comma for multiple expands
            location, quantity, meta, experiments
        sort : str, optional    
            Sort by a specific field
        checkedOut : str, optional
            Filter for checked out samples
        minimumQuantityAmount : str, optional
            Filter for samples that have a minimum quantity amount set
        name : str, optional
            Filter by sample name
        sampleTypeID : str, optional
            Filter by sampleTypeID  
        barcodes : str, optional
            Filter by barcodes (comma-separated)
        search : str, optional
            Search term to use for filtering samples. 
        quantityID : str, optional
            Filter by quantityID
        """    
        request = {}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["checkedOut", "name", "sampleTypeID", "barcodes", 
                       "search", "quantityID"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
                    check_arg = arg.first(True)
                if isinstance(check_arg,SampleType):
                    request["sampleTypeID"] = check_arg.id()
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
        return(Samples(self._eLABJournalObject__api, "Samples", "/api/v1/storage/"+urllib.parse.quote(str(self.id()))+"/samples", request, "sampleID", 5, self._eLABJournalObject__api.sample))
          
     
    