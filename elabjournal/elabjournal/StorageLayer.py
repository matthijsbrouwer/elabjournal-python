from .eLABJournalObject import *

class StorageLayer(eLABJournalObject):

    def __init__(self, api, data):
        """
        Internal use only: initialize storage object
        """
        if ((data is not None) & (type(data) == dict) & 
            ("name" in data)
           ):
            super().__init__(api, data, "storageLayerID", str(data["name"])) 
            if "storageID" in data.keys():
                self.__storageID = data["storageID"]
            else:
                self.__storageID = None     
        else:
            raise Exception("no (valid) storage layer data") 
        
    def visualize(self):
        """
        Create visualization.
        """
        g = super().visualize()
        
        storage = self.storage()
        
        if storage:
            storage_id = str(storage.id())
            storage_name = str(storage.name())
            with g.subgraph(name="cluster_storage") as g_storage:
                g_storage.attr(tooltip="storage", label="storageID "+storage_id, style="filled", color="black", fillcolor="#EEEEEE")
                g_storage.node("storage_name",storage_name, {"tooltip": "storage", "style": "filled", "fillcolor": "white", "shape": "rect"})                                       
            g.edge("storage_name", "class_name", None, {})          
        
            storage_type = storage.storage_type()        
            if storage_type:
                storage_type_id = str(storage_type.id())
                storage_type_name = str(storage_type.name())
                storage_type_type = str(storage_type.type())
                with g.subgraph(name="cluster_type") as g_type:
                    g_type.attr(tooltip="type of storage", label="storageTypeID "+storage_type_id, style="filled", color="black", fillcolor="#EEEEEE")
                    g_type.node("storage_type_name",storage_type_name, {"tooltip": "type of storage", "style": "filled", "fillcolor": "white", "shape": "rect"})                                       
                    g_type.node("storage_type_type",storage_type_type, {"tooltip": "type of storage", "style": "filled", "fillcolor": "white", "shape": "rect"})                                       
                g.edge("storage_type_type", "storage_name", None, {"constraint": "false"})
            
        return(g)              
        
    def parent(self):
        """
        Get the parent as an object.
        """
        if "parentStorageLayerID" in self.data():
            parentStorageLayerID = self.data()["parentStorageLayerID"]
            if parentStorageLayerID>0:
                return(self._eLABJournalObject__api.storage_layer(parentStorageLayerID))
        return None     
        
    def barcode(self):
        """
        Get the barcode of the storage layer.
        """
        if "barcode" in self.data():
            barcode = self.data()["barcode"]
            return(barcode)
        return None
        
    def storage(self):
        """
        Get the storage as an object.
        """
        if self.__storageID is not None:
            return self._eLABJournalObject__api.storage(self.__storageID)   
        return None     
        
    