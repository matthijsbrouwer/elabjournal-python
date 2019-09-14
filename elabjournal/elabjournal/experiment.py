from .eLABJournalObject import * 
from .Sections import *
from .Section import *

import pandas as pd
import matplotlib.figure
import urllib.parse
import numbers
import html
import openpyxl
from IPython.core.display import HTML

class Experiment(eLABJournalObject):

    def __init__(self, api, data):        
        """
        Internal use only: initialize experiment object.
        """
        if ((data is not None) & (type(data) == dict) & 
            ("name" in data.keys())
           ):
            super().__init__(api, data, "experimentID", str(data["name"])) 
        else:
            raise Exception("no (valid) experiment data") 
        
    def visualize(self):
        """
        Show visualization.
        """
        project = self._eLABJournalObject__api.project(self.data()["projectID"])
        project_id = str(project.id())
        project_name = str(project.name())
        study = self._eLABJournalObject__api.study(self.data()["studyID"])
        study_id = str(study.id())
        study_name = str(study.name())
        experiment_id = str(self.id())
        experiment_name = str(self.name()) 
        sections = self.sections(sort="order").all()      
        
        g = graphviz.Digraph()

        with g.subgraph(name="cluster_experiment") as g_experiment:
            g_experiment.attr(tooltip="experiment", label="experimentID "+experiment_id, style="filled", color="black", fillcolor="#067172", fontcolor="white")
            g_experiment.node("experiment_name",experiment_name, {"tooltip": "name of experiment", "style": "filled", "color": "#0B3B52", "fontcolor": "white", "shape": "rect"})                        
        
        with g.subgraph(name="cluster_study") as g_study:
            g_study.attr(tooltip="study", label="studyID "+study_id, style="filled", color="black", fillcolor="#EEEEEE")
            g_study.node("study_name",study_name, {"tooltip": "name of experiment", "style": "filled", "fillcolor": "white", "shape": "rect"})   
        
        with g.subgraph(name="cluster_project") as g_project:
            g_project.attr(tooltip="project", label="projectID "+project_id, style="filled", color="black", fillcolor="#EEEEEE")
            g_project.node("project_name",project_name, {"tooltip": "name of experiment", "style": "filled", "fillcolor": "white", "shape": "rect"})                        
        
        g.edge("project_name","study_name",None,{"constraint": "false"})
        g.edge("study_name","experiment_name",None,{"constraint": "false"})
        
        procedures = []
        samples = []
        with g.subgraph(name="cluster_sections") as g_sections:
            g_sections.attr(style="dashed,filled", fillcolor="white")
            for sectionID in sections.index:
                order = sections.loc[sectionID]["order"]
                type = str(sections.loc[sectionID]["sectionType"])
                name = str(sections.loc[sectionID]["sectionHeader"])
                with g_sections.subgraph(name="cluster_section_"+str(order)) as g_section:
                    g_section.attr(style="filled", fillcolor="#EEEEEE")
                    g_section.node("section_"+str(order)+"_name",name,{"group": "section_name", "style":"filled", "fillcolor":"white", "shape":"rect"})
                    g_section.node("section_"+str(order),str(order)+".",{"group": "section_order", "style":"filled", "fillcolor":"white", "shape":"ellipse"})
                    g_section.node("section_"+str(order)+"_type",type,{"group": "section_type", "style":"filled", "fillcolor":"white", "shape":"rect"})
                    g_section.node("section_"+str(order)+"_id","expJournalID\n"+str(sectionID),{"group": "section_id", "shape":"plaintext"})
                    g_section.edge("section_"+str(order)+"_id","section_"+str(order)+"_type",None,{"style": "invis", "constraint": "False"})
                    g_section.edge("section_"+str(order)+"_type","section_"+str(order),None,{"arrowhead": "none", "constraint": "False"})
                    g_section.edge("section_"+str(order),"section_"+str(order)+"_name",None,{"arrowhead": "none", "constraint": "False"})
                if order>1:
                    g_sections.edge("section_"+str(order-1),"section_"+str(order),None,{})
                else:
                    g_sections.edge("experiment_name","section_"+str(order),None,{"rank": "source"})
                if type=="PROCEDURE":
                    procedures.append(order)  
                elif (type=="SAMPLESIN") | (type=="SAMPLESOUT"):
                    samples.append(order)            
                
        if len(procedures)>0:                
            g.node("protocols","Procedures", {"style": "filled", "fillcolor": "lightyellow", "shape": "cylinder"})
            for order in procedures:
                g.edge("section_"+str(order)+"_name","protocols", None,{"arrowhead": "none", "rank": "same"})
        if len(samples)>0:                
            g.node("samples","Samples", {"style": "filled", "fillcolor": "lightyellow", "shape": "cylinder"})
            g.node("storage","Storage", {"style": "filled", "fillcolor": "lightyellow", "shape": "cylinder"})
            g.edge("storage","samples", None,{"arrowhead": "none", "rank": "same"})
            for order in samples:
                g.edge("section_"+str(order)+"_name","samples", None,{"arrowhead": "none", "rank": "same"})
                
        return(g)
        
        
    def show(self):
        """
        Show the content of this experiment.
        """
        sections = self.sections(sort="order").all()
        htmlCode = ""
        for id in sections.index:
            section = self.section(id)
            htmlCode += "<h2>"+html.escape(section.name())+"</h2><br/>"
            htmlCode += section.show().data
            htmlCode += "<br />"
        return(HTML(htmlCode))         
            
    def sections(self, *args, **kwargs):
        """
        Get object to access sections.
        
        Parameters (key/value)
        ----------------------
        expand : str, optional
            Expand an ID field to an object
        sort : str, optional    
            Sort by a specific field
        archived : str, optional
            Filter by archived or non-archived sections.
        """    
        request = {"$sort": "order"}
        kwargs_special = ["expand", "sort"]
        kwargs_keys = ["archived"]
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
        return(Sections(self._eLABJournalObject__api,"Experiment sections", 
                     "/api/v1/experiments/"+urllib.parse.quote(str(self.id()))+"/sections", request, "expJournalID", 5, self.section))
        
        
    def section(self, id):
        """
        Get within this experiment the section object with provided id.
        """ 
        request = {}
        if isinstance(id,numbers.Integral) | isinstance(id,str):
            section = self._eLABJournalObject__api.section(id)  
            if section is not None:
                #check experimentID
                if section.data()["experimentID"]==self.id():
                    return(section)
            return None
        else:
            raise Exception("incorrect call")    
    
    def add(self, data, title=None, order=None):
        """
        Add a new section to this experiment.
        """
        if data is None:
            return(None)
        elif isinstance(data, Section):
            sectionType = data.type()
            if title==None:
                sectionHeader = data.title()
            else:
                sectionHeader = title
            sectionData = data.get()    
        else:
            if title==None:
                sectionHeader = "New section"
            else:
                sectionHeader = title
            if isinstance(data, pd.DataFrame):
                sectionType = "DATATABLE"
                sectionData = data
            elif isinstance(data, matplotlib.figure.Figure):    
                sectionType = "CANVAS"
                sectionData = data
            elif isinstance(data, PngImagePlugin.PngImageFile):   
                sectionType = "CANVAS"
                sectionData = data
            elif isinstance(data, openpyxl.workbook.workbook.Workbook):   
                sectionType = "EXCEL"
                sectionData = data
            else:
                raise Exception("no (valid) section data")
        #create new section    
        request = {"sectionType": sectionType, "sectionHeader": sectionHeader}
        location = "/api/v1/experiments/"+urllib.parse.quote(str(self.id()))+"/sections"
        section_id = self._eLABJournalObject__api._request(location, "post", json.dumps(request))       
        #get new section
        new_section = self._eLABJournalObject__api.section(section_id)
        #put content in section
        new_section.set(sectionData)
        #return new section
        return(new_section)
        
            
            
        
        