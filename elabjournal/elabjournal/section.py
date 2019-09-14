from .eLABJournalObject import * 

from .SectionMetas import *

import json
import openpyxl
import pandas as pd
import matplotlib
import urllib.parse
import numbers
import base64
import html
from PIL import Image, PngImagePlugin
from IPython.core.display import HTML
from io import BytesIO

class Section(eLABJournalObject):

    def __init__(self, api, data):        
        """
        Internal use only: initialize section object.
        """
        if (not(data==None) & (type(data) == dict) & 
            ("experimentID" in data.keys()) & 
            ("sectionType" in data.keys()) & 
            ("sectionHeader" in data.keys())
           ):
            self.__experimentID = data["experimentID"]
            self.__sectionType = data["sectionType"]
            super().__init__(api, data, "expJournalID", str(data["sectionHeader"]))                                
        else:
            raise Exception("no (valid) section data") 
        
    def visualize(self):
        """
        Show visualization.
        """
        section_id = str(self.id())
        section_name = str(self.name()) 
        section_type = str(self.__sectionType)                
        experiment = self._eLABJournalObject__api.experiment(self.data()["experimentID"])
        experiment_id = str(experiment.id())
        experiment_name = str(experiment.name()) 
        project = self._eLABJournalObject__api.project(experiment.data()["projectID"])
        project_id = str(project.id())
        project_name = str(project.name())
        study = self._eLABJournalObject__api.study(experiment.data()["studyID"])
        study_id = str(study.id())
        study_name = str(study.name())
        
        g = graphviz.Digraph()

        with g.subgraph(name="cluster_section") as g_section:
            g_section.attr(tooltip="section", label="expJournalID "+section_id, style="filled", color="black", fillcolor="#067172", fontcolor="white")
            g_section.node("section_name",section_name, {"tooltip": "title of section", "style": "filled", "color": "#0B3B52", "fontcolor": "white", "shape": "rect"})                        
        
        with g.subgraph(name="cluster_experiment") as g_experiment:
            g_experiment.attr(tooltip="experiment", label="experimentID "+experiment_id, style="filled", color="black", fillcolor="#EEEEEE")
            g_experiment.node("experiment_name",experiment_name, {"tooltip": "name of experiment", "style": "filled", "fillcolor": "white", "shape": "rect"})                        
        
        with g.subgraph(name="cluster_study") as g_study:
            g_study.attr(tooltip="study", label="studyID "+study_id, style="filled", color="black", fillcolor="#EEEEEE")
            g_study.node("study_name",study_name, {"tooltip": "name of experiment", "style": "filled", "fillcolor": "white", "shape": "rect"})   
        
        with g.subgraph(name="cluster_project") as g_project:
            g_project.attr(tooltip="project", label="projectID "+project_id, style="filled", color="black", fillcolor="#EEEEEE")
            g_project.node("project_name",project_name, {"tooltip": "name of experiment", "style": "filled", "fillcolor": "white", "shape": "rect"})                        
        
        with g.subgraph(name="cluster_content") as g_content:
            g_content.attr(style="dashed,filled", color="black", fillcolor="white")
            with g_content.subgraph(name="cluster_sectiontype") as g_sectiontype:
                g_sectiontype.attr(style="filled", color="black", fillcolor="#EEEEEE")
                g_sectiontype.node("section_type",section_type, {"tooltip": "type of section", "style": "filled", "fillcolor": "white", "shape": "rect"})                             
                                                                                                                 
        metas = self.metas().all()
        if len(metas)>0:
            with g.subgraph(name="cluster_metas") as g_metas:
                htmlCode = "<<table bgcolor=\"#FFFFFF\" border=\"0\" cellborder=\"1\" cellspacing=\"0\">"
                htmlCode = htmlCode + "<tr><td><b>name</b></td><td><b>value</b></td></tr>"
                for metaID in metas.index:
                    meta_name = metas.loc[metaID]["name"]
                    meta_value = metas.loc[metaID]["val"]
                    htmlCode = htmlCode + "<tr><td>"+html.escape(meta_name)+"</td><td>"+html.escape(meta_value)+"</td></tr>"                
                htmlCode = htmlCode + "</table>>"
                g_metas.attr(labelloc="b", label=htmlCode, style="filled", color="black", fillcolor="#EEEEEE")                                          
                g_metas.node("metas","Metas",{"shape": "rect", "style": "filled", "fillcolor": "white"})                                    
            g.edge("project_name","metas",None,{"rank": "source", "style": "invis"})
            g.edge("study_name","metas",None,{"rank": "source", "style": "invis"})
            g.edge("experiment_name","metas",None,{"rank": "source", "style": "invis"})
            g.edge("section_name","metas",None,{"rank": "source", "style": "invis"})
            g.edge("section_type","metas",None,{"constraint": "false"})
                
        g.edge("project_name","study_name",None,{"constraint": "false"})
        g.edge("study_name","experiment_name",None,{"constraint": "false"})    
        g.edge("experiment_name","section_name",None,{"constraint": "false"})  
        g.edge("section_name","section_type",None,{})  
        
        return(g)  
        
    def show(self):
        """
        Show the content of the section.
        """
        htmlCode = "<div style=\"border: 1px solid #067172; padding: 10px;\">"
        htmlCode = htmlCode + "<b>Section type "+str(self.__sectionType)+" not implemented</b>"                                                    
        htmlCode = htmlCode + "</div>"                                                    
        return(HTML(htmlCode))      
    
    def type(self):
        """
        Get the type of the section.
        """ 
        return(self.__sectionType)
    
    def experiment(self):
        """
        Get the experiment containing this section.
        """ 
        return(self._eLABJournalObject__api.experiment(self.__experimentID))
        
    def meta(self, name, value=None):
        """
        Get or set meta item (meta) by name for the section.
        """
        if value==None:
            rp = self._eLABJournalObject__api._request("/api/v1/experiments/sections/"+urllib.parse.quote(str(self.id()))+"/meta/"+urllib.parse.quote(str(name)), "get", {}, show_messages=False)
            if not(rp==None) & (type(rp) == dict):
                if "name" in rp.keys() and rp["name"]==name:
                    return(rp)
                else:
                    return(None)                                                     
            else:
                return(None)
        elif type(value)==str:
            data = {"name": name, "val": value}
            rp = self._eLABJournalObject__api._request("/api/v1/experiments/sections/"+urllib.parse.quote(str(self.id()))+"/meta", "post", data)
            
        else:
            raise Exception("value must be string")     
   
        
    def metas(self, *args, **kwargs):
        """
        Get object to access metas.
        
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
                if isinstance(check_arg, eLABJournalPager):
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
        return(SectionMetas(self._eLABJournalObject__api,"Section meta items", 
                     "/api/v1/experiments/sections/"+urllib.parse.quote(str(self.id()))+"/meta", request, "expJournalMetaID", 5))
        
           
       
        