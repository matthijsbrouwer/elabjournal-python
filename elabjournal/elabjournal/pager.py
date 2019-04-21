import pandas as pd
import math
import ipywidgets as widgets
from IPython.display import display, clear_output
from pandas.io.json import json_normalize


class pager:

    def __init__(self, api, title, location, request, index, sort, records):        
        #store
        self.__api = api
        self.__title = title
        self.__location = location
        self.__request = request
        self.__index = index
        self.__sort = sort
        self.__records = records
        self._reset()
        #get first page        
        self._set_page(self.__page)  
        
    def _reset(self):
        self.__page = 0
        self.__maxRecords = 0
        self.__totalRecords = 0
        self.__pages = 0
        self.__data = None
        
    def __repr__(self):
        description = self.__title
        if self.__pages>1:
            return(description+" ("+str(self.__pages)+" pages)")
        else:
            return(description)
        
    def _set_page(self, page):
        #define request
        request = self.__request
        request["$page"] = page
        request["$records"] = self.__records
        request["$sort"] = self.__sort
        rp = self.__api.request(self.__location,"get",request)
        #check and get
        if rp==None:
            self._reset()
        elif type(rp) == dict:
            if "maxRecords" in rp.keys():
                self.__maxRecords = rp["maxRecords"]
            else:
                raise Exception("unexpected response, no maxRecords")
            if "totalRecords" in rp.keys():
                self.__totalRecords = rp["totalRecords"]
            else:
                raise Exception("unexpected response, no totalRecords")    
            if "currentPage" in rp.keys():
                self.__page = rp["currentPage"]
            else:
                raise Exception("unexpected response, no currentPage")
            self.__pages = math.ceil(self.__totalRecords/self.__maxRecords)  
            if "data" in rp.keys():                        
                self.__page = page
                self.__data = pd.DataFrame(json_normalize(rp["data"]))
                if len(self.__data)>0:
                    self.__data = self.__data.set_index(self.__index)                
            else:
                raise Exception("unexpected response, no data")                    
        else:
            raise Exception("unexpected response, no dict")         
    
    
    #todo: reset button
    def show(self):   
        #data
        data = widgets.Output()                              
        #paging
        box_layout = widgets.Layout(
            display='flex', flex_flow='row', justify_content='space-between', 
            border='solid', width='100%')
        children = []
        header = widgets.Label()    
        button_previous = widgets.Button(description="previous", button_style="primary")                        
        button_next = widgets.Button(description="next", button_style="primary")                        
        if self.__pages>1:
            children = [button_previous, header, button_next]
        else:
            children = [widgets.Label(),header,widgets.Label()]
        box = widgets.Box(children=children, layout=box_layout)        
        #output
        display(widgets.VBox((box,data)))
            
        #set header content    
        def set_header_and_buttons(page):  
            if self.__pages>1:
                header.value=self.__title+" - page "+str(page+1)+" of "+str(self.__pages)
                if page==0:
                    button_previous.disabled=True
                    button_previous.button_style=""
                else:
                    button_previous.disabled=False
                    button_previous.button_style="primary"
                if page==(self.__pages-1):
                    button_next.disabled=True
                    button_next.button_style="" 
                else:
                    button_next.disabled=False
                    button_next.button_style="primary"    
            else:
                header.value=self.__title
                
        #define actions on buttons    
        def on_button_previous(b):
            if self.__page>0:
                set_header_and_buttons(self.__page-1) 
                button_previous.disabled=True
                button_next.disabled=True
                self._set_page(self.__page-1) 
                set_header_and_buttons(self.__page) 
                with data:
                    clear_output();
                    display(self.__data) 
                
        def on_button_next(b):
            if self.__page<(self.__pages-1):
                set_header_and_buttons(self.__page+1) 
                button_previous.disabled=True
                button_next.disabled=True
                self._set_page(self.__page+1) 
                set_header_and_buttons(self.__page) 
                with data:
                    clear_output();
                    display(self.__data) 
                
        set_header_and_buttons(self.__page)    
        with data:
            display(self.__data)  
        button_previous.on_click(on_button_previous)
        button_next.on_click(on_button_next)
        
        
        
        
        
        
        