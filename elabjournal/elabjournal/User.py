from .eLABJournalObject import * 

import graphviz

class User(eLABJournalObject):

    def __init__(self, api, data):
        """
        Internal use only: initialize user object
        """
        if ((data is not None) & (type(data) == dict) & 
            ("firstName" in data) & 
            ("lastName" in data)
           ):
            name = str(data["firstName"])+" "+str(data["lastName"])
            super().__init__(api, data, "userID", name)            
        else:
            raise Exception("no (valid) User data") 
            
        
    def visualize(self):
        """
        Visualization user
        """
        g = graphviz.Digraph()
        #add user
        user_id = str(self.id())
        user_name = str(self.name())
        with g.subgraph(name="cluster_user") as g_user:
            g_user.attr(tooltip="user", label="userID "+user_id, style="filled", color="black", fillcolor="#067172", fontcolor="white")
            g_user.node("user_name",user_name, {"tooltip": "name of user", "style": "filled", "color": "#0B3B52", "fontcolor": "white", "shape": "rect"})
        #add group                
        group = self._eLABJournalObject__api.group()
        group_name = str(group.name())   
        group_id = str(group.id())
        with g.subgraph(name="cluster_group") as g_group:
            g_group.attr(labelloc="b", tooltip="active group", label="groupID "+group_id, style="dashed,filled", color="black", fillcolor="#EEEEEE")
            g_group.node("group_name",group_name, {"tooltip": "name of active group", "style": "filled", "color": "black", "fillcolor": "white", "shape": "rect"})                
        g.edge("user_name","group_name", None, {"style": "dashed"})        
        #add institute
        if "instituteID" in self._eLABJournalObject__data:
            institute_id = str(self._eLABJournalObject__data["instituteID"])
            institute_name = "Organisation"
            with g.subgraph(name="cluster_institute") as g_institute:
                g_institute.attr(labelloc="b", tooltip="organization", label="instituteID "+institute_id, style="dashed,filled", color="black", fillcolor="#EEEEEE")
                g_institute.node("institute_name",institute_name, {"tooltip": "name of organization", "style": "filled", "color": "black", "fillcolor": "white", "shape": "rect"})                
            g.edge("user_name","institute_name", None, {"style": "dashed"})
        #return graph
        return(g)            
        
    
        
      