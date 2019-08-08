from .eLABJournalObject import *

import graphviz
import requests

class ExperimentFile(eLABJournalObject):

    def __init__(self, api, data, response):
        """
        Internal use only: initialize f object
        """
        if ((data is not None) & (type(data) == dict) & 
            ("expJournalID" in data) & 
            ("realName" in data) & ("fileSize" in data) & 
            (response is not None) & 
            (type(response) == requests.models.Response) & 
            response.ok
           ):
            self.__size = data["fileSize"]
            self.__response = response
            super().__init__(api, data, "experimentFileID", str(data["realName"]))             
        else:
            raise Exception("no (valid) file data") 
        
    def visualize(self):
        """
        Visualization
        """
        file_id = str(self.id())
        file_name = str(self.name())
        storage = None
        if "hybridStorage.url" in self.data():
            storage = str(self.data()["hybridStorage.url"]).replace("http://","").replace("https://","").replace("/"," ").strip()            
        section = None
        if "expJournalID" in self.data():
            section = self._eLABJournalObject__api.section(self.data()["expJournalID"])
            section_id = str(section.id())
            section_name = str(section.title()) 
            experiment = self._eLABJournalObject__api.experiment(section.data()["experimentID"])
            experiment_id = str(experiment.id())
            experiment_name = str(experiment.name()) 
            project = self._eLABJournalObject__api.project(experiment.data()["projectID"])
            project_id = str(project.id())
            project_name = str(project.name())
            study = self._eLABJournalObject__api.study(experiment.data()["studyID"])
            study_id = str(study.id())
            study_name = str(study.name())
        else:
            section = None                        
        
        methodList = []
        for m in dir(self):
            if (not str(m).startswith("_")) & (not (str(m)=="visualize")):
                methodList.append(str(m))
         
        g = graphviz.Digraph()

        if section:
            with g.subgraph(name="cluster_section") as g_section:
                g_section.attr(tooltip="section", label="expJournalID "+section_id, style="filled", color="black", fillcolor="#EEEEEE")
                g_section.node("section_name",section_name, {"tooltip": "title of section", "style": "filled", "fillcolor": "white", "shape": "rect"})                        
            
            with g.subgraph(name="cluster_experiment") as g_experiment:
                g_experiment.attr(tooltip="experiment", label="experimentID "+experiment_id, style="filled", color="black", fillcolor="#EEEEEE")
                g_experiment.node("experiment_name",experiment_name, {"tooltip": "name of experiment", "style": "filled", "fillcolor": "white", "shape": "rect"})                        
            
            with g.subgraph(name="cluster_study") as g_study:
                g_study.attr(tooltip="study", label="studyID "+study_id, style="filled", color="black", fillcolor="#EEEEEE")
                g_study.node("study_name",study_name, {"tooltip": "name of experiment", "style": "filled", "fillcolor": "white", "shape": "rect"})   
            
            with g.subgraph(name="cluster_project") as g_project:
                g_project.attr(tooltip="project", label="projectID "+project_id, style="filled", color="black", fillcolor="#EEEEEE")
                g_project.node("project_name",project_name, {"tooltip": "name of experiment", "style": "filled", "fillcolor": "white", "shape": "rect"})
                
            g.edge("project_name","study_name",None,{"constraint": "false"})
            g.edge("study_name","experiment_name",None,{"constraint": "false"})    
            g.edge("experiment_name","section_name",None,{"constraint": "false"})  
            g.edge("section_name","file_name",None,{})                              
        
        with g.subgraph(name="cluster_file") as g_file:
            g_file.attr(tooltip="file", label="experimentFileID "+file_id, style="filled", color="black", fillcolor="#067172", fontcolor="white")
            g_file.node("file_name",file_name, {"tooltip": "name of file", "style": "filled", "color": "#0B3B52", "fontcolor": "white", "shape": "rect"})
                
        with g.subgraph(name="cluster_methods") as g_methods:   
            g_methods.attr(labelloc="b", style="filled", color="black", fillcolor="#EEEEEE", fontcolor="black", label="available methods")     
            for method in methodList:
                name="method_"+method
                label=method+"()"
                tooltip=getattr(self,method).__doc__.strip().splitlines()[0]
                g_methods.node(name,label,{"tooltip":tooltip, "style": "filled", "color": "black", "fontcolor": "black", "fillcolor": "white", "shape":"record"})        
                g_methods.edge("file_name",name,None,{"style": "dashed"}) 
                
        if storage:
            with g.subgraph(name="cluster_storage") as g_storage:
                g_storage.attr(style="dashed,filled", color="black", fillcolor="white")
                g_storage.node("storage",storage,{"tooltip": "storage", "shape": "rect", "style": "filled", "fillcolor": "white"})
            g.edge("file_name", "storage", None, {"style": "dashed", "arrowhead": "none", "constraint": "false"})
            if section: 
                g.edge("section_name", "storage", None, {"style": "invis"})
                g.edge("experiment_name", "storage", None, {"style": "invis"})
                g.edge("study_name", "storage", None, {"style": "invis"})
                g.edge("project_name", "storage", None, {"style": "invis"})
                
                
        return(g)
        
    def content(self):
        """
        Get the file content.
        """
        return(self.__response.content) 
        
    def headers(self):
        """
        Get headers for the file.
        """
        return(self.__response.headers)           
        
      