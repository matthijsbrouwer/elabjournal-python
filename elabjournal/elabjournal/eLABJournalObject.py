import graphviz
import html
from IPython.core.display import HTML

class eLABJournalObject:
 
 
    def __init__(self, api, data, id_key, name, title=None):
        """
        Internal use only: initialize object.
        """
        if ((data is not None) and (type(data) == dict) and (id_key in data.keys())):
            self.__id = data[id_key]
            self.__id_key = id_key
            self.__api = api
            self.__name = name        
            self.__data = data
            if title==None:
                self.__title = str(self.__class__.__name__)+" '"+str(name)+"' ("+str(data[id_key])+")"
            else:
                self.__title = title  
        else:
            raise Exception("no (valid) data") 

    def __repr__(self):
        """
        Internal use only: description object and available methods.        
        """ 
        text = str(self.__title).strip()
        text += self.__api._create_methods(self)     
        return(text)
        
    def id(self):
        """
        Get id.
        """
        return(self.__id)    
        
    def data(self):
        """
        Get data.
        """
        return(self.__data) 
        
    def visualize(self):
        """
        Create visualization.
        """
        g = graphviz.Digraph()
        with g.subgraph(name="cluster_object") as g_object:
            g_object.attr(tooltip=str(self.__class__.__name__), label=str(self.__id_key)+" "+str(self.__id), style="filled", color="black", fillcolor="#067172", fontcolor="white")
            g_object.node("class_name",str(self.name()), {"tooltip": str(self.__class__.__name__), "style": "filled", "color": "#0B3B52", "fontcolor": "white", "shape": "rect"})
            if hasattr(self, "type") and callable(getattr(self,"type")):
                g_object.node("class_type",str(self.type()), {"tooltip": "type", "style": "filled", "color": "#0B3B52", "fontcolor": "white", "shape": "rect"})                                                                               
        return(g) 
        
    def show(self, fields=None):
        """
        Create representation.
        
        Parameters
        ----------
        fields: list, optional
            A list of fields to limit the number of rows in the result
        """
        data = self.data()
        htmlCode = "<p><strong>"+html.escape(str(self.name()))+"</strong><br/>"
        htmlCode+= html.escape(str(self.__class__.__name__))+", id "+html.escape(str(self.id()))+"</p>"            
        if isinstance(data,dict):
            htmlCode+= "<table>\n"
            htmlCode+= "  <thead><tr><th>name</th><th>value</th></tr></thead>\n"
            htmlCode+= "  <tbody>\n"
            for key in data.keys():
                if (fields is None):
                    htmlCode+= "    "+self._show_object_row(key,data[key])            
                elif isinstance(fields,list) and (key in fields):
                    htmlCode+= "    "+self._show_object_row(key,data[key])            
            htmlCode+= "  </tbody>\n"
            htmlCode+= "<table>\n"
        return(HTML(htmlCode)) 
        
    def _show_object_row(self, key, value):
        htmlCode ="<tr>"
        htmlCode+="<td>"+html.escape(str(key))+"</td>"
        if isinstance(value,dict):
            htmlCode+="<td><table><thead><tr><th>name</th><th>value</th></tr></thead><tbody>"
            for subkey in value.keys():
                htmlCode+=self._show_object_row(subkey,value[subkey])
            htmlCode+="</tbody></table></td>"
        elif isinstance(value,list):
            htmlCode+="<td><table><thead><tr><th>number</th><th>value</th></tr></thead><tbody>"
            for i in range(len(value)):
                htmlCode+=self._show_object_row(i,value[i])
            htmlCode+="</tbody></table></td>"
        else:
            htmlCode+="<td>"+html.escape(str(value))+"</td>"
        return(htmlCode)            
    
    def name(self):
        """
        Get the name.
        """
        return(self.__name)
        
    def title(self):
        """
        Get the title.
        """
        return(self.__title)        
        
        