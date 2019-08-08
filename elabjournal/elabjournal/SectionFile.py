from .Section import * 
from .ExperimentFile import * 
from .ExperimentFiles import * 



class SectionFile(Section):

    def __init__(self, api, data):        
        """
        Internal use only: initialize section object.
        """
        if (not(data==None) & (type(data) == dict) & 
            ("sectionType" in data.keys()) 
           ):
             if data["sectionType"]=="FILE":
                 super().__init__(api, data)
             else:   
                 raise Exception("no file")                                         
        else:
            raise Exception("no (valid) section data") 
            
            
    def visualize(self):
        """
        Show visualization.
        """
        g = super().visualize()
        
        with g.subgraph(name="cluster_content") as g_content:
            files = self.get().all()
            storages = {}
            for fileID in files.index:  
                file_description = files.loc[fileID]["realName"]
                file_name = files.loc[fileID]["realName"]
                with g_content.subgraph(name="cluster_file_"+str(fileID)) as g_file:                                        
                    g_file.attr(labelloc="b", tooltip=file_description, label="experimentFileID "+str(fileID), style="filled", color="black", fillcolor="#EEEEEE")
                    g_file.node("file_"+str(fileID),file_name,{"tooltip": file_description, "shape":"rect", "style": "filled", "fillcolor": "white"})
                if "hybridStorage.url" in files.loc[fileID]:
                    file_storage = str(files.loc[fileID]["hybridStorage.url"]).replace("http://","").replace("https://","").replace("/"," ").strip()
                    if file_storage not in storages:
                        storages[file_storage] = []
                    storages[file_storage].append(fileID) 
                g_content.edge("section_type","file_"+str(fileID),None,{}) 
            if len(storages)>0:
                with g.subgraph(name="cluster_storages") as g_storages:
                    g_storages.attr(style="dashed,filled", color="black", fillcolor="white")
                    counter = 0
                    for storage in storages:
                        counter += 1
                        g_storages.node("storage_"+str(counter),storage,{"tooltip": "storage", "shape": "rect", "style": "filled", "fillcolor": "white"})
                        for fileID in storages[storage]:
                            g.edge("file_"+str(fileID), "storage_"+str(counter), None, {"style": "dashed", "arrowhead": "none", "rank": "same"}) 
        return(g)          
            
    def show(self):
        """
        Show the content.
        """
        files = self.get().all()
        htmlCode = "<div style=\"border: 1px solid #067172; padding: 10px;\">"
        for fileID in files.index:
            file_name = str(files.loc[fileID]["realName"])
            file_size = str(math.ceil(files.loc[fileID]["fileSize"]/1024))+" kb"
            g = graphviz.Digraph()
            with g.subgraph(name="cluster_file_"+str(fileID)) as g_file:
                g_file.attr(tooltip="experimentFileID "+str(fileID), label=file_size, style="filled", color="black", fillcolor="#067172", fontcolor="white")
                g_file.node("file_name_"+str(fileID),file_name, {"tooltip": "filename", "style": "filled", "color": "#0B3B52", "fontcolor": "white", "shape": "rect"})                                
            htmlCode = htmlCode+"<figure style=\"display: inline-block; margin-right: 10px; margin-bottom: 10px;\">"
            htmlCode = htmlCode+g.pipe(format="svg").decode("utf-8")
            htmlCode = htmlCode+"</figure>"
        htmlCode = htmlCode + "</div>"                                                    
        return(HTML(htmlCode))  
            
    def get(self):
        """
        Get the content of this section.
        """ 
        return(ExperimentFiles(self._eLABJournalObject__api, "Files", "/api/v1/experiments/sections/"+urllib.parse.quote(str(self.id()))+"/files", {}, "experimentFileID", 5, self.file))
        
        
    def file(self, id):
        """
        Get file with the provided id (integer or string) for this section.
        """
        if isinstance(id,numbers.Integral) | isinstance(id,str): 
            files = self.get().all()
            if id in files.index:
                fileData = files.loc[id].to_dict()
                fileData["experimentFileID"] = id
                fileData["expJournalID"] = self.id()
                if ("hybridStorage.localStorageRequest" in fileData) & ("hybridStorage.url" in fileData):                    
                    request = {"action": "download", "localStorageRequest": fileData["hybridStorage.localStorageRequest"]}
                    response = self._eLABJournalObject__api._request(fileData["hybridStorage.url"],"post",request,stream=True, headers={"Content-Type":"application/x-www-form-urlencoded"})
                    return(ExperimentFile(self._eLABJournalObject__api,fileData,response))
                else :
                    raise Exception("couldn't access storage for this file")     
            else:
                raise Exception("no file for this id")             
        else:
            raise Exception("incorrect call")                           
        
        
                                                                                            
            
    