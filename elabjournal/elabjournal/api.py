from .pager import *
from .experiment import *
from .section import *

import requests
import json
import keyring

def reset_key():
    keyring.delete_password("elabjournal-python", "apikey")   

class api:

    def __init__(self, key=None):
        
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
                        print("Welcome "+rp["user"]["firstName"]+" "+rp["user"]["lastName"])
                        self.__key = key
                        self.__user = rp["user"]
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
        
    
    def samples(self, search=None):
        request = {}
        if not(search==None):
            request["search"] = search
        return(pager(self, "Samples", "/api/v1/samples", request, "sampleID", None, 5))
    
    def sample_types(self, name=None, archived=None):
        request = {}
        if not(name==None):
            request["name"] = name
        if not(archived==None):
            request["archived"] = archived
        return(pager(self, "SampleTypes", "/api/v1/sampleTypes", request, "sampleTypeID", None, 5))
    
    def groups(self, search=None):
        request = {}
        if not(search==None):
            request["search"] = search
        return(pager(self, "Groups", "/api/v1/groups", request, "groupID", None, 5))
    
    def projects(self, search=None):
        request = {}
        if not(search==None):
            request["search"] = search
        return(pager(self, "Projects", "/api/v1/projects", request, "projectID", "projectID DESC", 5))
    
    def experiments(self, search=None):
        request = {}
        if not(search==None):
            request["search"] = search
        return(pager(self, "Experiments", "/api/v1/experiments", request, "experimentID", "experimentID DESC", 5))
    
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
    
    
    def __repr__(self):
        description = "eLABJournal API object"
        if self.__key == None:
            description += " - authentication failed"
        else:
            description += " - authenticated as "+self.__user["firstName"]+" "+self.__user["lastName"]
        return(description)    
        
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
        
        