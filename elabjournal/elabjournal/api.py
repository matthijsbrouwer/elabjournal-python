from .eLABJournalPager import *

from .Experiment import *
from .Experiments import *
from .Group import *
from .Groups import *
from .Project import *
from .Projects import *
from .Sample import *
from .Samples import *
from .SampleType import *
from .SampleTypes import *
from .SampleTypeMeta import *
from .SampleTypeMetas import *
from .SampleMeta import *
from .SampleMetas import *
from .SampleSerie import *
from .SampleSeries import *
from .SamplesAndSeries import *
from .Section import *
from .SectionParagraph import *
from .SectionProcedure import *
from .SectionDatatable import *
from .SectionCanvas import *
from .SectionExcel import *
from .SectionImage import *
from .SectionFile import *
from .SectionSample import *
from .Sections import *
from .Storage import *
from .Storages import *
from .StorageLayer import *
from .StorageLayers import *
from .StorageType import *
from .StorageTypes import *
from .Study import *
from .Studies import *
from .User import *

from .. import _version

import requests
import json
import keyring
import numbers
import urllib.parse
import pkg_resources
import graphviz
import inspect

def reset_key():
    keyring.delete_password("elabjournal-python", "apikey")   

class api:

    def __init__(self, key=None):
        """
        Internal use only: initialize API
        """        
        self.__key = None
        self.__timeout = 180
        self.__url = None
        self.__defaultUrl = "https://www.elabjournal.com"
        self.__user = None
        self.__version__ = _version.__version__
        
        def check_and_set_key(key, throw_error, store_valid_key):
            if key==None:            
                return(False)
            elif (type(key) == str) & (len(key)>0):
                #filter input
                if ";" in key:
                    key_url = "https://"+key.split(";",1)[0].strip()                    
                    key_key = key.split(";",1)[-1].strip()
                else:
                    key_url = self.__defaultUrl
                    key_key = key.split(";",1)[-1].strip()                                  
                try:
                    rp = self._request(key_url+"/api/v1/auth/user","get",{"body":{}},key_key)                   
                    if not(rp==None) & ("user" in rp.keys()):
                        self.__url = key_url
                        self.__key = key_key
                        self.__user = User(self, rp["user"])
                        welcomeText = "Welcome "+self.__user.name() + "\nPackage 'elabjournal', version '"+str(self.__version__)+"'"                     
                        if key_url != self.__defaultUrl:
                            welcomeText = welcomeText + "\nConnected to '" +str(key_url.split("://",1)[-1].strip()) + "'"
                        group = self.group()
                        if group is not None:
                            welcomeText = welcomeText + "\nYour active group is '" + str(group.name()) + "' (" + str(group.id()) + ")" 
                        print(welcomeText)
                        if store_valid_key:                                                
                            keyring.set_password("elabjournal-python", "apikey", key)                
                        return(True) 
                    else:
                        return(False)
                except:
                    return(False)
            else:
                return(False)               
        
        if key == None:
            keyring_key = keyring.get_password("elabjournal-python", "apikey")
            if not(check_and_set_key(keyring_key, False, False)):        
                from IPython.display import clear_output
                key = str(input("REST API key: "))
                clear_output();
                check_and_set_key(key, True, True)                                
        else:
          check_and_set_key(key, True, False)       
        
    
    def __repr__(self):
        """
        Internal use only: description API object
        """ 
        text = "eLABJournal API object - version "+self.__version__
        if self.__key == None:
            text += " - authentication failed"
        else:
            text += " - authenticated as "+self.__user.name()
        text += self._create_methods(self)                     
        return(text) 
        
    def visualize(self):
        """
        Show visualization.
        """
        user_name = self.__user.name()
        group_name = str(self.group().name())
        group_id = str(self.group().id())
        sample_types_number = str(self.sample_types().number())
        samples_number = str(self.samples().number())
        storage_types_number = str(self.storage_types().number())
        storages_number = str(self.storages(deviceType="STORAGE").number())
        storage_layers_number = str(self.storage_layers().number())
        projects_number = str(self.projects().number())
        studies_number = str(self.studies().number())
        experiments_number = str(self.experiments().number())
                        
        g = graphviz.Digraph()

        with g.subgraph(name="cluster_elabjournal") as g_elabjournal:
            g_elabjournal.attr(label="eLABJournal - authentication", style="filled", color="#000000", fillcolor="#067172", fontcolor="#FFFFFF")
            g_elabjournal.node("groups","groups",{"shape": "folder", "style":"filled", "fillcolor":"lightyellow"})
            with g_elabjournal.subgraph(name='cluster_elabjournal_user') as g_elabjournal_user:
                g_elabjournal_user.node("user",user_name, {"tooltip": "Authenticated user, this should be you!", "style": "filled", "color": "#0B3B52", "fontcolor": "#FFFFFF", "shape": "rect"})
                g_elabjournal_user.node("group",group_name, {"tooltip": "Active group ("+group_id+") for "+user_name, "style": "filled", "color": "#EF7900", "shape": "rect"})
                g_elabjournal_user.edge("user", "group", None, {"style": "dotted", "color": "#FFFFFF", "arrowhead": "none"})
                g_elabjournal_user.attr(label="", color="#FFFFFF", style="dashed,filled", fillcolor="#08A1A1")
                g_elabjournal_user.node("point_elabjournal_user","",{"shape":"none", "width": "0", "height": "0"})
            g_elabjournal.edge("user","groups",None,{"color": "#000000"}) 
            g_elabjournal.edge("groups","group",None,{"color": "#000000", "constraint": "false"}) 
                
        
        
        with g.subgraph(name="cluster_group") as g_group:
            g_group.attr(label="Group '"+group_name+"'", style="dashed,filled", color="#000000", fillcolor="#EEEEEE")
            with g_group.subgraph(name="cluster_group_experiments") as g_group_experiments:
                g_group_experiments.node("projects","Projects ("+projects_number+"x)",{"tooltip": "Available with projects() method", "shape": "folder", "style":"filled", "fillcolor":"lightyellow"})
                g_group_experiments.node("studies","Studies ("+studies_number+"x)",{"tooltip": "Available with studies() method", "shape": "folder", "style":"filled", "fillcolor":"lightyellow"})
                g_group_experiments.node("experiments","Experiments ("+experiments_number+"x)",{"tooltip": "Available with experiments() method", "shape": "rect", "style":"filled", "fillcolor":"white"})
                g_group_experiments.edge("projects", "studies", None, {})
                g_group_experiments.edge("studies", "experiments", None, {})
                g_group_experiments.attr(label="Journal", color="#000000", fontcolor="#FFFFFF", style="dashed,filled", fillcolor="#08A1A1")
            with g_group.subgraph(name="cluster_group_samples") as g_group_samples:    
                g_group_samples.node("sampletypes","Sample types ("+sample_types_number+"x)",{"tooltip": "Available with sample_types() method", "shape": "folder", "style":"filled", "fillcolor":"lightyellow"})
                g_group_samples.node("samples","Samples ("+samples_number+"x)",{"tooltip": "Available with samples() method", "shape": "rect", "style":"filled", "fillcolor":"white"})
                g_group_samples.edge("sampletypes", "samples", None, {})
                g_group_samples.attr(label="Samples", color="#000000", fontcolor="#FFFFFF", style="dashed,filled", fillcolor="#08A1A1")
            with g_group.subgraph(name="cluster_group_storages") as g_group_storages:    
                g_group_storages.node("storagetypes","Storage types ("+storage_types_number+"x)",{"tooltip": "Available with storage_types() method", "shape": "folder", "style":"filled", "fillcolor":"lightyellow"})
                g_group_storages.node("storages","Storages ("+storages_number+"x)",{"tooltip": "Available with storages() method", "shape": "folder", "style":"filled", "fillcolor":"lightyellow"})
                g_group_storages.node("storagelayers","Storage layers ("+storage_layers_number+"x)",{"tooltip": "Available with storage_layers() method", "shape": "rect", "style":"filled", "fillcolor":"white"})
                g_group_storages.edge("storagetypes", "storages", None, {})
                g_group_storages.edge("storages", "storagelayers", None, {})
                g_group_storages.attr(label="Storage", color="#000000", fontcolor="#FFFFFF", style="dashed,filled", fillcolor="#08A1A1")  
            g_group.edge("samples", "storagelayers", None, {"color": "#000000", "constraint": "false"})    
            g_group.edge("experiments", "samples", None, {"color": "#000000", "constraint": "false"})    
            g_group.node("point_group","",{"shape":"none", "width": "0", "height": "0"})
            
        g.edge("point_elabjournal_user","point_group",None,{"color": "#000000", "rank": "source"})        
                
        return(g)
        
    
    def version(self):
        """
        Get the version of the package.
        """
        return(self.__version__)
     
    def user(self):
        """
        Get the current user.
        """
        return(self.__user)
        
    def barcode(self, barcode):
        """
        Get object for the provided barcode.
        """ 
        if isinstance(barcode,numbers.Integral) | isinstance(barcode,str): 
            rp = self._request("/api/v1/barcode/"+urllib.parse.quote(str(barcode)), "get", {})
            #check and get
            if (rp is not None) & (type(rp) == dict) & ("type" in rp):
                if rp["type"]=="SAMPLE":
                    return(self.sample(rp["id"]))                    
                elif rp["type"]=="SAMPLESERIES":   
                    return(self.sample_serie(rp["id"]))                 
                elif rp["type"]=="STORAGELAYER":   
                    return(self.storage_layer(rp["id"]))                 
                else:
                    raise Exception("unknown type "+rp["type"])                                                     
            else:
                return(None)    
        else:
            raise Exception("incorrect call")       
     
    def samples(self, *args, **kwargs):
        """
        Get object to access samples.
        
        Parameters (object)
        ----------------------
        class: parser
            Pass the result of the first() method on this object instead
        class: sample_type
            Filter by sampleTypeID of this object 
        class: storage
            Filter by storageID of this object     
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
            separate values with comma for multiple expands
            location, quantity, meta, experiments, parent, children
        sort : str, optional    
            Sort by a specific field
        storageLayerID : str, optional
            Filter for samples in a storage layer
        sampleTypeID : str, optional
            Filter by sampleTypeID  
        name : str, optional
            Filter by sample name
        barcodes : str, optional
            Filter by barcodes (comma-separated)
        archived : str, optional
            Filter by archived or non-archived samples. 
            If set to true the search parameter has no effect
        quantityID : str, optional
            Filter by quantityID
        minimumQuantityAmount : str, optional
            Filter for samples that have a minimum quantity amount set
        checkedOut : str, optional
            Filter for checked out samples
        storageID : str, optional
            Filter for samples in a storage unit
        search : str, optional
            Search term to use for filtering samples. 
            This parameter can't be combined with archived=true
        """    
        request = {}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["storageLayerID", "sampleTypeID", "name", "barcodes", 
                       "archived", "quantityID", "minimumQuantityAmount", "checkedOut", 
                       "storageID", "search"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
                    check_arg = arg.first(True)
                if isinstance(check_arg,SampleType):
                    request["sampleTypeID"] = check_arg.id()
                elif isinstance(check_arg,Storage):
                    request["storageID"] = check_arg.id()    
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
        return(Samples(self, "Samples", "/api/v1/samples", request, "sampleID", 5, self.sample))
    
    def sample(self, id):
        """
        Get sample object with provided id or get multiple sample objects with provided id.
        """ 
        if isinstance(id,numbers.Integral) | isinstance(id,str): 
            rp = self._request("/api/v1/samples/"+urllib.parse.quote(str(id)), "get", {})
            #check and get
            if (rp is not None) & (type(rp) == dict):
                return(Sample(self,rp))                                                 
            else:
                return(None)    
        elif isinstance(id,list):
            request = {"sampleID": ",".join(map(str,id))}
            return(Samples(self, "Samples", "/api/v1/samples/get", request, "sampleID", 5, self.sample))                                        
        else:
            raise Exception("incorrect call")         
                
    def create_sample(self, *args, **kwargs):
        """
        Create a sample.
        
        Parameters (object)
        ----------------------
        class: parser
            Pass the result of the first() method on this object instead
        class: sample_type
            Pass the sampleTypeID of this object 
        class: sample
            Pass the sampleID of this object as parentSampleID
        class: storage_layer
            Pass the storageLayerID of this object as storageLayerID
                
        
        Parameters (key/value)
        ----------------------
        name : str, optional
            Name of the new sample
        sampleTypeID : integer, optional
            Define sampleType of the new sample                  
        checkedOut: boolean, optional
            Define checkedOut status
        parentSampleID : integer, optional
            Define parentSample of the new sample
        description : str, optional
            Description for the new sample
        note : str, optional
            Note for the new sample
        altID : str, optional
            Alternative ID for the new sample
        storageLayerID : integer, optional
            Define storage layer for the new sample
        position : integer, optional
            Define position of the new sample               
        
        """ 
        request = {}
        kwargs_obligatory = ["name", "sampleTypeID"]
        kwargs_keys = ["checkedOut", "parentSampleID", "description", "note", "altID", "storageLayerID", "position"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
                    check_arg = arg.first(True)
                if isinstance(check_arg,SampleType):
                    request["sampleTypeID"] = check_arg.id()
                elif isinstance(check_arg,Sample):
                    request["parentSampleID"] = check_arg.id()    
                elif isinstance(check_arg,StorageLayer):
                    request["storageLayerID"] = check_arg.id()    
                else:
                    raise Exception("unsupported object '"+str(type(check_arg))+"'")                 
        if kwargs is not None:
            for key, value in kwargs.items():
                if key in kwargs_obligatory:
                    request[key] = value   
                elif key in kwargs_keys:
                    request[key] = value
                else:
                    raise Exception("unsupported key '"+key+"'") 
        for key in kwargs_obligatory:
            if key not in request:
                raise Exception("'"+key+"' must be provided")             
        rp = self._request("/api/v1/samples/", "post", request)
        if not (rp == ""):
            return(self.sample(rp))
        else:    
            return(None)   
            
    def update_sample(self, id, *args, **kwargs):
        """
        Update the sample with the provided id.
        
        Parameters (object)
        ----------------------
        class: parser
            Pass the result of the first() method on this object instead
        class: sample
            Pass the sampleID of this object as parentSampleID
        class: storage_layer
            Pass the storageLayerID of this object as storageLayerID
                
        
        Parameters (key/value)
        ----------------------
        name : str, optional
            Name of the new sample
        parentSampleID : integer, optional
            Define parentSample of the new sample
        description : str, optional
            Description for the new sample
        note : str, optional
            Note for the new sample
        altID : str, optional
            Alternative ID for the new sample
        storageLayerID : integer, optional
            Define storage layer for the new sample
        position : integer, optional
            Define position of the new sample            
        
        """ 
        request = {}
        kwargs_keys = ["name", "parentSampleID", "description", "note", "altID", "storageLayerID", "position"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
                    check_arg = arg.first(True)
                if isinstance(check_arg,Sample):
                    request["parentSampleID"] = check_arg.id()    
                elif isinstance(check_arg,StorageLayer):
                    request["storageLayerID"] = check_arg.id()    
                else:
                    raise Exception("unsupported object '"+str(type(check_arg))+"'")                 
        if kwargs is not None:
            for key, value in kwargs.items():
                if key in kwargs_keys:
                    request[key] = value
                else:
                    raise Exception("unsupported key '"+key+"'") 
        if(len(request)>0):           
            rp = self._request("/api/v1/samples/"+urllib.parse.quote(str(id)), "patch", request)
            if not (rp == ""):
                return(self.sample(id))
            else:    
                return(None)  
        else:
            raise Exception("nothing to update")                                   
        
    def delete_sample(self, *args, **kwargs):
        """
        Delete a sample.
        
        Parameters (object)
        ----------------------
        class: sample
            Delete this sample
                
        
        Parameters (key/value)
        ----------------------
        id : str
            Delete the sample with this sampleID             
        
        """ 
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,Sample):
                    id = check_arg.id()    
                else:
                    raise Exception("unsupported object '"+str(type(check_arg))+"'")                 
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "id":
                    id = value
                else:
                    raise Exception("unsupported key '"+key+"'")                
        if isinstance(id,numbers.Integral) | isinstance(id,str):             
            rp = self._request("/api/v1/samples/"+urllib.parse.quote(str(id)), "delete", {})            
        else:
            raise Exception("incorrect call")             
        
    def sample_metas(self, id):
        """
        Get object to access sampleMetas for sample with provided id.
        """ 
        request = {}
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            sample = self.sample(id)
            if (sample is not None):                
                return(SampleMetas(self, "SampleMetas", "/api/v1/samples/"+urllib.parse.quote(str(id))+"/meta", request, "sampleMetaID", 5, sample.meta))
            else:
                return(None)    
        else:
            raise Exception("incorrect call")
                             
    def sample_meta(self, sample_id, sample_meta_id):
        """
        Get sample meta object for provided sample_id and sample_meta_id.
        """ 
        if (isinstance(sample_id,numbers.Integral) | isinstance(sample_id,str)) & (isinstance(sample_meta_id,numbers.Integral) | isinstance(sample_meta_id,str)):
            rp = self._request("/api/v1/samples/"+urllib.parse.quote(str(sample_id))+"/meta/"+urllib.parse.quote(str(sample_meta_id)), "get", {}) 
            #check and get
            if not(rp==None) & (type(rp) == dict):
                return(SampleMeta(self,sample_id,rp))                                                 
            else:
                return(None)                   
        else:
            raise Exception("incorrect call")
            
    def create_sample_meta(self, *args, **kwargs):
        """
        Create the sample meta
        
        Parameters (object)
        ----------------------
        class: parser
            Pass the result of the first() method on this object instead
        class: sample
            Pass the sampleID of this object  
        class: sample_meta
            Pass the sampleMetaID of this object      
                
        
        Parameters (key/value)
        ----------------------
        sampleID: str, required
            ID of the sample
        sampleIDs: str, optional
            Comma separated list of (linked) sampleIDs    
        fileIDs: str, optional
            Comma separated list of (linked) fileIDs    
        key: str, optional
            Key for the meta item
        value: str, optional
            Value for the meta item   
        sampleTypeMetaID: str, optional
            ID of the sampleType meta item                         
        
        """ 
        request = {}
        required = {}
        kwargs_obligatory = ["sampleID", "key","sampleDataType"]
        kwargs_keys = ["value", "sampleTypeMetaID"]
        kwargs_explode_keys = ["sampleIDs","fileIDs"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
                    check_arg = arg.first(True)
                if isinstance(check_arg,Sample):
                    request["sampleID"] = check_arg.id()
                else:    
                    raise Exception("unsupported object '"+str(type(check_arg))+"'")                 
        if kwargs is not None:
            for key, value in kwargs.items():
                if key in kwargs_obligatory:
                    request[key] = value
                elif key in kwargs_keys:
                    request[key] = value
                elif key in kwargs_explode_keys:
                    request[key] = str(value).split(",")
                else:
                    raise Exception("unsupported key '"+key+"'") 
        for key in kwargs_obligatory:
            if key not in request:
                raise Exception("'"+key+"' must be provided")                                              
        #fix request
        sampleID = request["sampleID"]
        del request["sampleID"]  
        rp = self._request("/api/v1/samples/"+urllib.parse.quote(str(sampleID))+"/meta", "post", request)
        try:
            sampleMetaID = int(rp)
            if sampleMetaID>0:
                return(self.sample_meta(sampleID, sampleMetaID))
            else:
                raise Exception("couldn't create meta")  
        except:
            print(rp)
            raise Exception("couldn't create meta")                                          
                             
    def update_sample_meta(self, *args, **kwargs):
        """
        Update the sample meta.
        
        Parameters (object)
        ----------------------
        class: parser
            Pass the result of the first() method on this object instead
        class: sample
            Pass the sampleID of this object  
        class: sample_meta
            Pass the sampleMetaID of this object      
                
        
        Parameters (key/value)
        ----------------------
        sampleID: str, required
            ID of the sample
        sampleMetaID: str, required
            ID of the sample_meta
        sampleIDs: str, optional
            Comma separated list of (linked) sampleIDs    
        fileIDs: str, optional
            Comma separated list of (linked) fileIDs    
        key: str, required
            Key for the meta item
        value: str, optional
            Value for the meta item    
        sampleMetaID: str, optional
            ID of the sampleType meta item                               
        
        """ 
        request = {}
        required = {}
        kwargs_obligatory = ["sampleID", "sampleMetaID"]
        kwargs_keys = ["key", "value", "sampleTypeMetaID"]
        kwargs_explode_keys = ["sampleIDs","fileIDs"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
                    check_arg = arg.first(True)
                if isinstance(check_arg,Sample):
                    request["sampleID"] = check_arg.id()
                elif isinstance(check_arg,SampleMeta):
                    request["sampleMetaID"] = check_arg.id()    
                else:    
                    raise Exception("unsupported object '"+str(type(check_arg))+"'")                 
        if kwargs is not None:
            for key, value in kwargs.items():
                if key in kwargs_obligatory:
                    required[key] = value
                elif key in kwargs_keys:
                    request[key] = value
                elif key in kwargs_explode_keys:
                    request[key] = str(value).split(",")
                else:
                    raise Exception("unsupported key '"+key+"'") 
        for key in kwargs_obligatory:
            if key not in required:
                raise Exception("'"+key+"' must be provided")                                
        if(len(request)>0):           
            rp = self._request("/api/v1/samples/"+urllib.parse.quote(str(required["sampleID"]))+"/meta/"+urllib.parse.quote(str(required["sampleMetaID"])), "patch", request)
            return(rp)              
        else:
            raise Exception("nothing to update")                              
                             
    def delete_sample_meta(self, *args, **kwargs):
        """
        Delete the sample meta.
        
        Parameters (object)
        ----------------------
        class: parser
            Pass the result of the first() method on this object instead
        class: sample
            Pass the sampleID of this object  
        class: sample_meta
            Pass the sampleMetaID of this object          
        
        Parameters (key/value)
        ----------------------
        sampleID: str, required
            ID of the sample
        key : str, required
            Key for the meta item
        value : str, optional
            Value for the meta item                        
        
        """ 
        required = {}
        kwargs_obligatory = ["sampleID", "sampleMetaID"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
                    check_arg = arg.first(True)
                if isinstance(check_arg,Sample):
                    required["sampleID"] = check_arg.id()
                elif isinstance(check_arg,SampleMeta):
                    required["sampleMetaID"] = check_arg.id()    
                elif isinstance(check_arg,int):
                    required["sampleMetaID"] = check_arg    
                else:    
                    raise Exception("unsupported object '"+str(type(check_arg))+"'")                 
        if kwargs is not None:
            for key, value in kwargs.items():
                if key in kwargs_obligatory:
                    required[key] = value
                else:
                    raise Exception("unsupported key '"+key+"'") 
        for key in kwargs_obligatory:
            if key not in required:
                raise Exception("'"+key+"' must be provided")                                
        rp = self._request("/api/v1/samples/"+urllib.parse.quote(str(required["sampleID"]))+"/meta/"+urllib.parse.quote(str(required["sampleMetaID"])), "delete", {})
        return(rp)                              
                             
    def sample_series(self, *args, **kwargs):
        """
        Get object to access sample series.
        
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
                if isinstance(check_arg,eLABJournalPager):
                    check_arg = arg.first(True)
                if isinstance(check_arg,SampleType):
                    request["sampleTypeID"] = check_arg.id()
                elif isinstance(check_arg,Storage):
                    request["storageID"] = check_arg.id()    
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
        return(SampleSeries(self, "SampleSeries", "/api/v1/sampleSeries", request, "seriesID", 5, self.sample_serie))        
                             
    def sample_serie(self, id):
        """
        Get sample serie object with provided id.
        """ 
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            rp = self._request("/api/v1/sampleSeries/"+urllib.parse.quote(str(id)), "get", {}) 
            #check and get
            if not(rp==None) & (type(rp) == dict):
                return(SampleSerie(self,rp))                                                 
            else:
                return(None)                   
        else:
            raise Exception("incorrect call")
                             
    def samples_and_series(self, *args, **kwargs):
        """
        Get object to access samples and series in aggregated list.
        
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
            location
        sort : str, optional    
            Sort by a specific field
        sampleTypeID : str, optional
            Filter by sampleTypeID  
        name : str, optional
            Filter by sample name
        search : str, optional
            Search term to use for filtering samples. 
        """    
        request = {}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["expand", "sampleTypeID", "name", "search"]
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
        return(SamplesAndSeries(self, "Samples and Series", "/api/v1/samplesAndSeries", request, ["type", "sampleID", "seriesID"], 5, self.sample_or_serie))
    
    def sample_or_serie(self, type, sample_id, sample_serie_id):
        """
        Get sample serie or serie object (based on provided type) with provided sample_id or sample_serie_id.
        """ 
        if type=="SERIES":
            return(self.sample_serie(sample_serie_id))
        elif type=="SAMPLE":
            return(self.sample(sample_id))
        else:
            raise Exception("incorrect call")
    
    def sample_types(self, *args, **kwargs):
        """
        Get object to access sample types.
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
        sort : str, optional    
            Sort by a specific field
        name : str, optional
            Filter by sample name
        archived : str, optional
            Filter by archived or non-archived samples.
        """    
        request = {}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["name", "archived"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
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
        return(SampleTypes(self, "SampleTypes", "/api/v1/sampleTypes", request, "sampleTypeID", 5, self.sample_type))
        
    def sample_type(self, id):
        """
        Get sample type object for provided sample_type_id or sample object.
        """ 
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            rp = self._request("/api/v1/sampleTypes/"+urllib.parse.quote(str(id)), "get", {}) 
            #check and get
            if not(rp==None) & (type(rp) == dict):
                return(SampleType(self,rp))                                                 
            else:
                return(None)
        elif isinstance(id,sample):
            return id_object.sampleType()
        else:
            raise Exception("incorrect call")
            
    def sample_type_metas(self, id):
        """
        Get object to access sampleTypeMetas for sample with provided id.
        """ 
        request = {}
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            return(SampleTypeMetas(self, "SampleTypeMetas", "/api/v1/sampleTypes/"+urllib.parse.quote(str(id))+"/meta", request, ["sampleTypeID", "sampleTypeMetaID"], 5, self.sample_type_meta))
        else:
            raise Exception("incorrect call")
                             
    def sample_type_meta(self, sample_type_id, sample_type_meta_id):
        """
        Get sample type meta object with provided sample_type_id and sample_type_meta_id.
        """ 
        if (isinstance(sample_type_id,numbers.Integral) | isinstance(sample_type_id,str)) & (isinstance(sample_type_meta_id,numbers.Integral) | isinstance(sample_type_meta_id,str)):
            rp = self._request("/api/v1/sampleTypes/"+urllib.parse.quote(str(sample_type_id))+"/meta/"+urllib.parse.quote(str(sample_type_meta_id)), "get", {}) 
            #check and get
            if not(rp==None) & (type(rp) == dict):
                return(SampleTypeMeta(self,rp))                                                 
            else:
                return(None)
        else:
            raise Exception("incorrect call")
                             
    def storages(self, *args, **kwargs):
        """
        Get object to access storages.
        
        Parameters (object)
        ----------------------
        class: parser
            Pass the result of the first() method on this object instead
        class: storage_type
            Filter by storageTypeID of this object 
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
            separate values with comma for multiple expands
            storageLayer, managers
        sort : str, optional    
            Sort by a specific field
        storageTypeID : str, optional
            Filter by storageTypeID
        name : str, optional
            Filter by name
        storageTypeName : str, optional
            Filter by the storageType name
        deviceType : str, optional
            Filter by the storage type's device type (STORAGE or EQUIPMENT)
        """    
        request = {}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["storageTypeID", "name", "storageTypeName", 
                       "deviceType"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
                    check_arg = arg.first(True)
                if isinstance(check_arg, StorageType):
                    request["storageTypeID"] = check_arg.id()
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
        return(Storages(self, "Storages", "/api/v1/storage", request, "storageID", 5, self.storage))
    
    
    def storage(self, id, **kwargs):
        """
        Get storage object with provided id.
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
            separate values with comma for multiple expands
            storageLayer, managers, statistics
        """ 
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            request = {}
            kwargs_special = ["expand"]
            kwargs_keys = []
            if kwargs is not None:
                for key, value in kwargs.items():
                    if key in kwargs_special:
                        request["$"+key] = value   
                    elif key in kwargs_keys:
                        request[key] = value
                    else:
                        raise Exception("unsupported key '"+key+"'")   
            
            rp = self._request("/api/v1/storage/"+urllib.parse.quote(str(id)), "get", request) 
            #check and get
            if (rp is not None) & (type(rp) == dict):
                return(Storage(self,rp))                                                 
            else:
                return(None)                   
        else:
            raise Exception("incorrect call")
            
    def groups(self, *args, **kwargs):
        """
        Get all groups that you have joined.
        """
        request = {}
        return(Groups(self, "Joined groups", "/api/v1/groups", request, "groupID", 5))
    
    def group(self):
        """
        Get the active group.
        """
        rp = self._request("/api/v1/groups/active", "get", {}) 
        #check and get
        if not(rp==None) & (type(rp) == dict):
            return(Group(self,rp))                                                 
        else:
            return(None)
            
    def set_group(self, id):
        """
        Set the active group to the provided id.
        """
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            self._request("/api/v1/groups/active", "put", str(id), headers={"Content-Type": "application/json"})            
        elif isinstance(id,Group):
            self._request("/api/v1/groups/active", "put", str(id.id()), headers={"Content-Type": "application/json"})  
        else:
            raise Exception("incorrect call")                                 
    
    def projects(self, *args, **kwargs):
        """
        Get object to access projects.
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
        sort : str, optional    
            Sort by a specific field
        search : str, optional
            Search experiments by name or contents
        """    
        request = {"$sort": "projectID DESC"}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["search"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
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
        return(Projects(self, "Projects", "/api/v1/projects", request, "projectID", 5, self.project))
        
    def project(self, id):
        """
        Get project object with provided id .
        """ 
        return(self._project(id,0))
        
    def _project(self, id, page):
        """
        Workaround to get project
        """ 
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            request = {"$page": int(page)}
            rp = self._request("/api/v1/projects", "get", request)
            #check and get
            if not(rp==None) & (type(rp) == dict):
                if ("totalRecords" in rp.keys()) & ("maxRecords" in rp.keys()) & (rp["totalRecords"]>=1):
                    maxPage = math.ceil(rp["totalRecords"]/rp["maxRecords"])
                    if "data" in rp.keys():
                        for dataItem in rp["data"]:
                            if(dataItem["projectID"]==id):
                                return(Project(self, dataItem))
                        page+=1
                        if page < maxPage:
                            return(self.project(id,page))
                        else:        
                            return(None)               
                    else:   
                        return(None)
                else:
                    return(None)                                                  
            else:
                return(None)  
        else:
            raise Exception("incorrect call")
              
    
    def experiments(self, *args, **kwargs):
        """
        Get object to access experiments.
        
        Parameters (object)
        ----------------------
        class: parser
            Pass the result of the first() method on this object instead
        class: project
            Filter by projectID of this object         
        class: study
            Filter by studyID of this object 
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
        sort : str, optional    
            Sort by a specific field
        studyID : str, optional
            Filter by study    
        projectID : str, optional
            Filter by project   
        search : str, optional
            Search experiments by name or contents
        """    
        request = {"$sort": "experimentID DESC"}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["studyID", "projectID", "search"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
                    check_arg = arg.first(True)
                if isinstance(check_arg,Project):
                    request["projectID"] = check_arg.id()
                elif isinstance(check_arg,Study):
                    request["studyID"] = check_arg.id()
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
        return(Experiments(self, "Experiments", "/api/v1/experiments", request, "experimentID", 5, self.experiment))
    
    def studies(self, *args, **kwargs):
        """
        Get object to access studies.
        
        Parameters (object)
        ----------------------
        class: parser
            Pass the result of the first() method on this object instead
        class: project
            Filter by projectID of this object 
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
        sort : str, optional    
            Sort by a specific field
        studyID : str, optional
            Filter by studyID
        search : str, optional
            Search experiments by name or contents
        projectID : str, optional
            Filter by projectID
        """    
        request = {"$sort": "studyID DESC"}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["studyID", "search", "projectID"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
                    check_arg = arg.first(True)
                if isinstance(check_arg,Project):
                    request["projectID"] = check_arg.id()
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
        return(Studies(self,"Studies", "/api/v1/studies", request, "studyID", 5, self.study))
    
    def study(self, id, **kwargs):
        """
        Get study object with provided id.
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
        """ 
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            request = {"studyID": str(id)}
            kwargs_special = ["expand"]
            kwargs_keys = []
            if kwargs is not None:
                for key, value in kwargs.items():
                    if key in kwargs_special:
                        request["$"+key] = value   
                    elif key in kwargs_keys:
                        request[key] = value
                    else:
                        raise Exception("unsupported key '"+key+"'")   
            
            rp = self._request("/api/v1/studies", "get", request) 
            #check and get
            if (rp is not None) & isinstance(rp,dict) & ("data" in rp) & isinstance(rp["data"],list) & (len(rp["data"])==1):
                return(Study(self,rp["data"][0]))                                                 
            else:
                return(None)                   
        else:
            raise Exception("incorrect call")
    
    
    def storage_types(self, *args, **kwargs):
        """
        Get object to access storageTypes.
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
        sort : str, optional    
            Sort by a specific field
        deviceType : str, optional
            Filter by the storage type's device type (STORAGE or EQUIPMENT)
        """    
        request = {}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["deviceType"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
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
        return(StorageTypes(self,"Storage Types", "/api/v1/storageTypes", request, "storageTypeID", 5, self.storage_type))
    
    def storage_type(self, id):
        """
        Get storage type object with provided id.
        """ 
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            rp = self._request("/api/v1/storageTypes/"+urllib.parse.quote(str(id)), "get", {}) 
            #check and get
            if not(rp==None) & (type(rp) == dict):
                return(StorageType(self,rp))                                                 
            else:
                return(None)                   
        else:
            raise Exception("incorrect call")                                 
    
    def storage_layers(self, *args, **kwargs):
        """
        Get object to access storageLayers.
        
        Parameters (object)
        ----------------------
        class: parser
            Pass the result of the first() method on this object instead
        class: storage_layer
            Filter by storageLayerID of this object as parent
        class: storage
            Filter by storageID of this object     
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
            separate values with comma for multiple expands
            storage, location, storageLayers, samples, managers, reservations / allReservations            
        sort : str, optional    
            Sort by a specific field
        name : str, optional    
            Filter by name
        barcodes : str, optional    
            Filter by barcodes (comma-separated)
        parentStorageLayerID : str, optional    
            Filter by parentStorageLayerID
        storageID : str, optional    
            Filter by storageID
        """    
        request = {}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["name","barcodes","parentStorageLayerID","storageID","deviceType"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if isinstance(check_arg,eLABJournalPager):
                    check_arg = arg.first(True)
                if isinstance(check_arg,Storage):
                    request["storageID"] = check_arg.id()
                elif isinstance(check_arg,StorageLayer):
                    request["parentStorageLayerID"] = check_arg.id()
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
        return(StorageLayers(self,"Storage Layers", "/api/v1/storageLayers", request, "storageLayerID", 5, self.storage_layer))
    
    def storage_layer(self, id, **kwargs):
        """
        Get storage layer object with provided id.
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
            separate values with comma for multiple expands
            storage, location, storageLayers, samples, managers, reservations / allReservations, statistics            
        """ 
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            request = {}
            kwargs_special = ["expand"]
            kwargs_keys = []
            if kwargs is not None:
                for key, value in kwargs.items():
                    if key in kwargs_special:
                        request["$"+key] = value   
                    elif key in kwargs_keys:
                        request[key] = value
                    else:
                        raise Exception("unsupported key '"+key+"'")   
            
            rp = self._request("/api/v1/storageLayers/"+urllib.parse.quote(str(id)), "get", request) 
            #check and get
            if not(rp==None) & (type(rp) == dict):
                return(StorageLayer(self,rp))                                                                
            else:
                return(None)                   
        else:
            raise Exception("incorrect call")                                 
    
    
    def experiment(self, id):
        """
        Get experiment object with provided id.
        """ 
        return(self._experiment(id,0))
    
    def _experiment(self, id, page):
        """
        Workaround to get experiment
        """ 
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            request = {"$page": int(page)}
            rp = self._request("/api/v1/experiments", "get", request)
            #check and get
            if not(rp==None) & (type(rp) == dict):
                if ("totalRecords" in rp.keys()) & ("maxRecords" in rp.keys()) & (rp["totalRecords"]>=1):
                    maxPage = math.ceil(rp["totalRecords"]/rp["maxRecords"])
                    if "data" in rp.keys():
                        for dataItem in rp["data"]:
                            if(dataItem["experimentID"]==id):
                                return(Experiment(self, dataItem))
                        page+=1
                        if page < maxPage:
                            return(self.experiment(id,page))
                        else:        
                            return(None)               
                    else:   
                        return(None)
                else:
                    return(None)                                                  
            else:
                return(None)
        else:
            raise Exception("incorrect call")        
        
    def section(self, section_id):
        """
        Get section object with provided id.
        """ 
        rp = self._request("/api/v1/experiments/sections/"+urllib.parse.quote(str(section_id)), "get", {})
        #check and get
        if not(rp==None) & (type(rp) == dict):
            if "sectionType" in rp:
                section_type = str(rp["sectionType"])
                if section_type == "PARAGRAPH":
                    return(SectionParagraph(self,rp))
                elif section_type == "PROCEDURE":
                    return(SectionProcedure(self,rp))
                elif section_type == "DATATABLE":
                    return(SectionDatatable(self,rp))
                elif section_type == "CANVAS":
                    return(SectionCanvas(self,rp))
                elif section_type == "EXCEL":
                    return(SectionExcel(self,rp))
                elif section_type == "IMAGE":
                    return(SectionImage(self,rp))
                elif section_type == "FILE":
                    return(SectionFile(self,rp))
                elif section_type == "SAMPLESIN":
                    return(SectionSample(self,rp))
                elif section_type == "SAMPLESOUT":
                    return(SectionSample(self,rp))
                else:
                    return(Section(self,rp))
            else:
                raise Exception("no sectionType in response")                                                 
        else:
            return(None)        
    
    def _request(self, location, method, request, key=None, show_messages=True, stream=False, headers=None):  
        if not location.startswith("http"):
            request_location = self.__url+location
        else:
            request_location = location            
        if key==None:
            key = self.__key
        try: 
            request_headers = {"Accept": "application/json"}
            request_headers.update({"Authorization": key})    
            if not(headers==None):
                request_headers.update(headers)
            if method=="get":
                if isinstance(request,dict):
                    data = request
                else:
                    raise Exception("unsupported type of request") 
                response = requests.get(request_location, params=data, timeout=self.__timeout, headers=request_headers, stream=stream)
            elif method=="post":  
                if "Content-Type" in request_headers:
                    data = request
                elif isinstance(request,str):
                    request_headers.update({"Content-Type": "application/json"})
                    data = request
                elif isinstance(request,dict):
                    request_headers.update({"Content-Type": "application/json"})
                    data = json.dumps(request)
                else:
                    raise Exception("unsupported type of request") 
                response = requests.post(request_location, data=data, timeout=self.__timeout, headers=request_headers, stream=stream)                
            elif method=="put":    
                if isinstance(request,str) | isinstance(request,bytes):
                    data = request
                else:
                    raise Exception("unsupported type of request") 
                response = requests.put(request_location, data=data, timeout=self.__timeout, headers=request_headers, stream=stream)                
            elif method=="patch":    
                if isinstance(request,str):
                    request_headers.update({"Content-Type": "application/json"})
                    data = request
                elif isinstance(request,dict):
                    request_headers.update({"Content-Type": "application/json"})
                    data = json.dumps(request)
                else:
                    raise Exception("unsupported type of request") 
                response = requests.patch(request_location, data=data, timeout=self.__timeout, headers=request_headers, stream=stream)                
            elif method=="delete":
                if isinstance(request,dict):
                    data = request
                else:
                    raise Exception("unsupported type of request") 
                response = requests.delete(request_location, params=data, timeout=self.__timeout, headers=request_headers, stream=stream)
            else:
                raise Exception("unsupported method")   
            response.raise_for_status() 
            #no content
            if response.status_code == 204:
                return(None)
            elif stream:
                return(response)
            else:    
                try:
                    return(json.loads(response.text))
                except json.JSONDecodeError as decodeErr:
                    print ("JSON Decode Error:",decodeErr) 
                    raise Exception("no (valid) response from eLABJournal")            
        except requests.exceptions.HTTPError as httpErr: 
            if show_messages:
                print ("Http Error:",httpErr) 
            try:
                return(json.loads(response.text))
            except json.JSONDecodeError as decodeErr:
                return(None)           
        except requests.exceptions.ConnectionError as connErr: 
            if show_messages:
                print ("Error Connecting:",connErr) 
            return(None)
        except requests.exceptions.Timeout as timeOutErr: 
            if show_messages:
                print ("Timeout Error:",timeOutErr) 
            return(None)
        except requests.exceptions.RequestException as reqErr: 
            if show_messages:
                print ("Something Else:",reqErr) 
            return(None)
        raise Exception("no (valid) response from eLABJournal")   
        
    def _create_methods(self, o):
        """
        Internal use only: create methods for object
        """ 
        text = "\n"
        text += "|\n"
        text += "|  Available methods, use help() on this object for more detailed information:\n"
        text += "|\n"
        methodList = []
        maxLength = 0
        for m in dir(o):
            if callable(getattr(o,m)) & (not str(m).startswith("_")):
                methodDoc = str(getattr(o,m).__doc__).strip().splitlines()[0]
                fullArgs = inspect.getfullargspec(getattr(o,m))
                methodArguments = fullArgs.args
                methodArguments.pop(0) #remove self
                if fullArgs.varargs:
                    methodArguments.append("*args")
                if fullArgs.varkw:
                    methodArguments.append("**kwargs")
                methodFull = str(m)+"("+(", ".join(str(arg) for arg in methodArguments))+")"
                methodList.append([m,methodFull,methodDoc])
        for m in methodList:        
            text += "|  "+m[1]+"\n"
            text += "|    "+m[2]+"\n"                         
        return(text)           
        
        