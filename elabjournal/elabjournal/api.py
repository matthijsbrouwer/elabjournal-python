from .pager import *
from .experiment import *
from .section import *
from .group import *
from .sample_type import *
from .sample_type_meta import *
from .sample import *
from .sample_meta import *
from .sample_serie import *

import requests
import json
import keyring
import numbers

def reset_key():
    keyring.delete_password("elabjournal-python", "apikey")   

class api:

    def __init__(self, key=None):
        """
        Internal use only: initialize API
        """        
        self.__key = None
        self.__timeout = 180
        self.__url = "https://www.elabjournal.com"
        self.__user = None
        
        def check_and_set_key(key, throw_error, store_valid_key):
            if key==None:            
                return(False)
            elif (type(key) == str) & (len(key)>0):
                try:
                    rp = self.request("/api/v1/auth/user","get",{"body":{}},key)                   
                    if not(rp==None) & ("user" in rp.keys()):
                        self.__key = key
                        self.__user = rp["user"]
                        welcomeText = "Welcome "+rp["user"]["firstName"]+" "+rp["user"]["lastName"]                        
                        group = self.group_active()
                        if group is not None:
                            welcomeText = welcomeText + ", your active group is '" + str(group.name()) + "' (" + str(group.id()) + ")" 
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
        description = "eLABJournal API object"
        if self.__key == None:
            description += " - authentication failed"
        else:
            description += " - authenticated as "+self.__user["firstName"]+" "+self.__user["lastName"]
        return(description)    
            
    def samples(self, *args, **kwargs):
        """
        Get object to access samples.
        
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
                if type(check_arg)==pager:
                    check_arg = arg.first(True)
                if type(check_arg)==sample_type:
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
        return(pager(self, "Samples", "/api/v1/samples", request, "sampleID", None, 5, self.sample))
    
    def sample(self, id):
        """
        Get sample object with provided id (integer or string) or get multiple sample
        objects with provided id (list).
        """ 
        if isinstance(id,numbers.Integral) | isinstance(id,str): 
            rp = self.request("/api/v1/samples/"+str(id), "get", {})
            #check and get
            if (rp is not None) & (type(rp) == dict):
                return(sample(self,rp))                                                 
            else:
                return(None)    
        elif isinstance(id,list):
            request = {"sampleID": ",".join(map(str,id))}
            rp = self.request("/api/v1/samples/get/", "get", request)
            result = {}
            if (rp is not None) & isinstance(rp,list):
                for item in rp:
                    if isinstance(item,dict) & ("sampleID" in item.keys()):
                        result[item["sampleID"]] = sample(self,item)                           
            return(result)                                  
        else:
            raise Exception("incorrect call")         
                
        
    def sample_metas(self, id):
        """
        Get object to access sampleMetas for sample with provided id (integer or string).
        """ 
        request = {}
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            sample = self.sample(id)
            if (sample is not None):                
                return(pager(self, "SampleMetas", "/api/v1/samples/"+str(id)+"/meta", request, "sampleMetaID", None, 5, sample.meta))
            else:
                return(None)    
        else:
            raise Exception("incorrect call")
                             
    def sample_meta(self, sample_id, sample_meta_id):
        """
        Get sample meta object for sample with provided sample_id (integer or string)
        and with provided sample_meta_id (integer or string) for the sample meta object.
        """ 
        if (isinstance(sample_id,numbers.Integral) | isinstance(sample_id,str)) & (isinstance(sample_meta_id,numbers.Integral) | isinstance(sample_meta_id,str)):
            rp = self.request("/api/v1/samples/"+str(sample_id)+"/meta/"+str(sample_meta_id), "get", {}) 
            #check and get
            if not(rp==None) & (type(rp) == dict):
                return(sample_meta(self,rp))                                                 
            else:
                return(None)                   
        else:
            raise Exception("incorrect call")
                             
    def sample_series(self):
        """
        Get object to access sampleSeries.
        """ 
        request = {}
        return(pager(self, "SampleSeries", "/api/v1/sampleSeries", request, "seriesID", None, 5, self.sample_serie))        
                             
    def sample_serie(self, id):
        """
        Get sample serie object with provided id (integer or string).
        """ 
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            rp = self.request("/api/v1/sampleSeries/"+str(id), "get", {}) 
            #check and get
            if not(rp==None) & (type(rp) == dict):
                return(sample_serie(self,rp))                                                 
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
                if type(check_arg)==pager:
                    check_arg = arg.first(True)
                if type(check_arg)==sample_type:
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
        return(pager(self, "Samples and Series", "/api/v1/samplesAndSeries", request, ["type", "sampleID", "seriesID"], None, 5, self.sample_or_serie))
    
    def sample_or_serie(self, type, sample_id, sample_serie_id):
        """
        Get sample serie or serie object based on provided type (SAMPLE/SERIES)
        with provided sample_id (integer or string) or sample_serie_id (integer or string).
        """ 
        if type=="SERIES":
            return(self.sample_serie(sample_serie_id))
        elif type=="SAMPLE":
            return(self.sample(sample_id))
        else:
            raise Exception("incorrect call")
    
    def sample_types(self, *args, **kwargs):
        """
        Get object to access sampleTypes.
        
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
                if type(check_arg)==pager:
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
        return(pager(self, "SampleTypes", "/api/v1/sampleTypes", request, "sampleTypeID", None, 5, self.sample_type))
        
    def sample_type(self, id):
        """
        Get sampleType object with provided id (integer or string) or
        return the sampleType for a sample if a sample object is provided.
        """ 
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            rp = self.request("/api/v1/sampleTypes/"+str(id), "get", {}) 
            #check and get
            if not(rp==None) & (type(rp) == dict):
                return(sample_type(self,rp))                                                 
            else:
                return(None)
        elif isinstance(id,sample):
            return id_object.sampleType()
        else:
            raise Exception("incorrect call")
            
    def sample_type_metas(self, id):
        """
        Get object to access sampleTypeMetas for sample with provided id (integer or string).
        """ 
        request = {}
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            return(pager(self, "SampleTypeMetas", "/api/v1/sampleTypes/"+str(id)+"/meta", request, ["sampleTypeID", "sampleTypeMetaID"], None, 5, self.sample_type_meta))
        else:
            raise Exception("incorrect call")
                             
    def sample_type_meta(self, sample_type_id, sample_type_meta_id):
        """
        Get sampleTypeMeta object with provided sample_type_id (integer or string) and
        sample_type_meta_id (integer or string).
        """ 
        if (isinstance(sample_type_id,numbers.Integral) | isinstance(sample_type_id,str)) & (isinstance(sample_type_meta_id,numbers.Integral) | isinstance(sample_type_meta_id,str)):
            rp = self.request("/api/v1/sampleTypes/"+str(sample_type_id)+"/meta/"+str(sample_type_meta_id), "get", {}) 
            #check and get
            if not(rp==None) & (type(rp) == dict):
                return(sample_type_meta(self,rp))                                                 
            else:
                return(None)
        else:
            raise Exception("incorrect call")
                             
    def groups(self, *args, **kwargs):
        """
        Get all groups that you have joined.
        """
        request = {}
        return(pager(self, "Groups", "/api/v1/groups", request, "groupID", None, 5))
    
    def group_active(self):
        """
        Get the active group.
        """
        rp = self.request("/api/v1/groups/active", "get", {}) 
        #check and get
        if not(rp==None) & (type(rp) == dict):
            return(group(self,rp))                                                 
        else:
            return(None)
    
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
        request = {}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["search"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if type(check_arg)==pager:
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
        return(pager(self, "Projects", "/api/v1/projects", request, "projectID", "projectID DESC", 5))
    
    def experiments(self, *args, **kwargs):
        """
        Get object to access experiments.
        
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
        request = {}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["studyID", "projectID", "search"]
        if args is not None:
            for arg in args:
                check_arg = arg
                if type(check_arg)==pager:
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
        return(pager(self, "Experiments", "/api/v1/experiments", request, "experimentID", "experimentID DESC", 5, self.experiment))
    
    def studies(self, search=None):
        request = {}
        if not(search==None):
            request["search"] = search
        return(pager(self,"Studies", "/api/v1/studies", request, "studyID", "studyID DESC", 5))
    
    def storage_types(self, search=None):
        request = {}
        if not(search==None):
            request["search"] = search
        return(pager(self,"Storage Types", "/api/v1/storageTypes", request, "storageTypeID", "storageTypeID DESC", 5))
    
    def experiment(self, experiment_id):
        request = {"$expand": experiment_id}
        rp = self.request("/api/v1/experiments", "get", request)
        #check and get
        if not(rp==None) & (type(rp) == dict):
            if ("totalRecords" in rp.keys()) & (rp["totalRecords"]>=1):
                if "data" in rp.keys():
                    if(rp["totalRecords"]==1):
                        return(experiment(self, rp["data"][0]))
                    else:
                        for dataItem in rp["data"]:
                            if(dataItem["experimentID"]==experiment_id):
                                return(experiment(self, dataItem))
                        return(None)               
                else:   
                    return(None)
            else:
                return(None)                                                  
        else:
            return(None)
        
    def section(self, section_id):
        rp = self.request("/api/v1/experiments/sections/"+str(section_id), "get", {})
        #check and get
        if not(rp==None) & (type(rp) == dict):
            return(section(self,rp))                                                 
        else:
            return(None)    
    
    
    def request(self, location, method, request, key=None, show_messages=True, stream=False, headers=None):  
        if key==None:
            key = self.__key
        try: 
            request_headers = {"Accept": "application/json"}
            request_headers.update({"Authorization": key})    
            if not(headers==None):
                request_headers.update(headers)
            if method=="get":
                if type(request) == dict:
                    data = request
                else:
                    raise Exception("unsupported type of request") 
                response = requests.get(self.__url+location, params=data, timeout=self.__timeout, headers=request_headers, stream=stream)
            elif method=="post":    
                if type(request) == str:
                    request_headers.update({"Content-Type": "application/json"})
                    data = request
                else:
                    raise Exception("unsupported type of request") 
                response = requests.post(self.__url+location, data=data, timeout=self.__timeout, headers=request_headers, stream=stream)                
            elif method=="put":    
                if (type(request) == str) | (type(request) == bytes):
                    data = request
                else:
                    raise Exception("unsupported type of request") 
                response = requests.put(self.__url+location, data=data, timeout=self.__timeout, headers=request_headers, stream=stream)                
            else:
                raise Exception("unsupported method")   
            response.raise_for_status() 
            #no content
            if response.status_code == 204:
                return(None)
            elif stream:
                return(response.content)
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
        
        