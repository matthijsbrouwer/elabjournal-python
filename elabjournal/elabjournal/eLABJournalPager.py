import pandas as pd
import math
import ipywidgets as widgets
import warnings
import graphviz
from IPython.display import display, clear_output


class eLABJournalPager:

    def __init__(self, api, title, location, request, index, records, item_handler=None):        
        """
        Internal use only: initialize pager object: general object to browse items.
        
        Parameters
        ----------
        api: api
            The api object
        title: str
            Title for the set of items
        location: str
            Prefix for REST api call url
        request: dict
            Parameters to add to REST api call url
        index: str / list
            Fields from response to be used as index.
            Also used as parameters for optional item_handler.
        records: int
            Number of items on each page when browsing the response.
        item_handler: method, optional
            Method to be used to get an item.            
        """
        #store
        self.__api = api
        self.__title = title
        self.__location = location
        self.__request = request
        self.__index = index
        self.__records = records
        self.__item_handler = item_handler
        self.__page = 0
        self.__list_response = False
        self._reset()
        #get first page        
        self._set_page(self.__page, records) 
        #define first
        if len(self.__data)>0:
            self.__first = self.__data.index.values[0]
        else:
            self.__first = None     
            
    def _reset(self):
        """
        Internal use only: reset pager object.
        """ 
        self.__page = 0
        self.__maxRecords = 0
        self.__totalRecords = 0
        self.__pages = 0
        self.__data = None
        
    def __repr__(self):
        """
        Internal use only: description pager object.
        """ 
        text = str(self.__title)+" ("+str(self.__totalRecords)+"x)"
        text += self.__api._create_methods(self)                                    
        return(text)
              
        
    def _set_page(self, page, records):
        """
        Internal use only: change page.
        """ 
        #define request
        request = self.__request
        if not self.__list_response:
            request["$page"] = page
            request["$records"] = records
        rp = self.__api._request(self.__location,"get",request)
        #check and get
        if rp==None:
            self._reset()
        elif isinstance(rp,dict):
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
                self.__data = pd.DataFrame(pd.json_normalize(rp["data"]))
                if len(self.__data)>0:
                    self.__data = self._filter_page(self.__data.set_index(self.__index))                
            else:
                raise Exception("unexpected response, no data")                    
        elif isinstance(rp,list):
            self.__list_response = True
            self.__maxRecords = records
            self.__totalRecords = len(rp)
            self.__page = page
            self.__data = pd.DataFrame(pd.json_normalize(rp))
            if len(self.__data)>0:
                self.__data = self._filter_page(self.__data.set_index(self.__index))
            start = self.__maxRecords*self.__page
            if start<len(self.__data):
                self.__data = self.__data.iloc[start:]
            elif start>0:
                self.__data = pd.DataFrame() 
            if len(self.__data)>self.__maxRecords:
                self.__data = self.__data.head(self.__maxRecords) 
            self.__pages = math.ceil(self.__totalRecords/self.__maxRecords)                            
        else:
            raise Exception("unexpected response")  
            
    def _filter_page(self, data):
        """
        Internal use only: filter page (flatten specific json).
        """ 
        dropList = set()
        numberTypes = {}
        for key in data.index:
            value = data.loc[key]
            for subkey in value.index:
                subvalue = value.loc[subkey]
                if isinstance(subvalue, list):
                    couldFindReplace=False
                    replace = {}
                    for item in subvalue:
                        if isinstance(item,dict):
                            couldFindReplace=True
                            if "key" in item:
                                for itemKey in item:
                                    if not(itemKey=="key"):
                                        newItemKey = str(item["key"])+"."+str(itemKey)
                                        if newItemKey in replace:
                                            replace[newItemKey].append(item[itemKey])
                                        else:
                                            replace[newItemKey] = [item[itemKey]]                                        
                            else:
                                for itemKey in item:
                                    if itemKey in replace:
                                        replace[itemKey].append(item[itemKey])
                                    else:
                                        replace[itemKey] = [item[itemKey]]                                                                
                    for replaceKey in replace.keys():
                        replaceValue = replace[replaceKey]
                        if len(replaceValue)==1:
                            replace[replaceKey] = replaceValue[0]
                        data.loc[key,str(subkey)+"."+str(replaceKey)] = str(replace[replaceKey])
                    if couldFindReplace:
                        data.loc[key,str(subkey)+".number"] = str(len(subvalue)) 
                        numberTypes[str(subkey)+".number"] = int
                        dropList.add(subkey)                        
        for numberType in numberTypes:
            data[numberType] = data[numberType].fillna(0).astype(numberTypes[numberType])        
        if len(dropList)>0:                       
            data = data.drop(columns=list(dropList))
        return(data)  
        
    def visualize(self):
        """
        Show visualization.
        """         
        g = graphviz.Digraph()
        with g.subgraph(name="cluster_pager") as g_pager:
            g_pager.attr(tooltip=str(self.__title), label=str(self.__title), style="filled", color="black", fillcolor="#067172", fontcolor="white")
            g_pager.node("pager",str(self.__totalRecords)+" item"+("s" if (self.__totalRecords!=1) else ""), {"tooltip": "number of objects", "style": "filled", "color": "#0B3B52", "fontcolor": "white", "shape": "rect"})        
        return(g)  
        
    def name(self):
        """
        Get the name.
        """
        return(self.__title)
        
    def title(self):
        """
        Get the title.
        """
        text = str(self.__title)+" ("+str(self.__totalRecords)+"x)"
        return(text)           
    
    def first(self, single=False):  
        """
        Get the first item (if exists).
        Raise an exception if `single` is set to True and the object describes 
        multiple items.
        
        If an `item_handler` is defined, this will be
        used to return an object. Otherwise the index for the first
        item will be returned (usually the ID).
        """ 
        if not((self.__item_handler is None) | (self.__first==None)):
            if single & (self.__totalRecords>1):
                raise Exception("multiple entries found ("+str(self.__totalRecords)+")")
            if isinstance(self.__first, tuple):
                return self.__item_handler(*self.__first)
            else:         
                return self.__item_handler(self.__first)
        else:    
            return(self.__first)
            
    def number(self):
        """
        Get the number of items.
        """   
        return(self.__totalRecords)   
            
    def fields(self):
        """
        Get the available fields.
        """   
        return(self.__data.columns.values.tolist())   
            
    def get(self, *args):
        """
        Get the item for the provided index entry.
        Only available if an `item_handler` is defined.
        This will also return items that are not contained within the scope of this object!
        """   
        if self.__item_handler is None:
            raise Exception("method not available")
        else:
           return self.__item_handler(*args)    
            
    def all(self, fields=None, maximum=None):
        """
        Return all items in a single DataFrame.
        
        Parameters
        ----------
        fields: list
            A list of fields to limit the number of columns in the result
        maximum: int
            A maximum to limit the number of rows in the result            
        """         
        if maximum is None:
            records =  100
        else:
            records = min(100, maximum)  
        recordCounter = 0                 
        page = 0
        dataSets = []
        while True:
            #define request
            request = self.__request
            request["$page"] = page
            request["$records"] = records
            rp = self.__api._request(self.__location,"get",request)
            if rp==None:
                return None;
            elif isinstance(rp,dict):
                if "maxRecords" in rp.keys():
                    maxRecords = rp["maxRecords"]
                else:
                    raise Exception("unexpected response, no maxRecords")
                if "totalRecords" in rp.keys():
                    totalRecords = rp["totalRecords"]
                else:
                    raise Exception("unexpected response, no totalRecords")    
                if "currentPage" in rp.keys():
                    page = rp["currentPage"]
                else:
                    raise Exception("unexpected response, no currentPage")
                pages = math.ceil(totalRecords/maxRecords)  
            if self.__list_response:    
                data = pd.DataFrame(pd.json_normalize(rp)) 
                #only if data
                if len(data)>0:
                    data = data.set_index(self.__index) 
                    data = self._filter_page(data)
                    #filter columns
                    if not(fields==None):
                        intersectList = [x for x in fields if x in data.columns.values]
                        dropList = [x for x in data.columns.values if x not in intersectList]
                        data = data.drop(columns=dropList)[intersectList]
                    if maximum is None:    
                        dataSets.append(data)
                    else:
                        if len(data) <= maximum:
                            dataSets.append(data)
                        else:
                            dataSets.append(data.head(maximum-len(data)))                              
                break                
            elif "data" in rp.keys():                        
                data = pd.DataFrame(pd.json_normalize(rp["data"]))                
                #only if data
                if len(data)>0:
                    data = data.set_index(self.__index) 
                    data = self._filter_page(data)
                    #filter columns
                    if not(fields==None):
                        intersectList = [x for x in fields if x in data.columns.values]
                        dropList = [x for x in data.columns.values if x not in intersectList]
                        data = data.drop(columns=dropList)[intersectList]
                    if maximum is None:    
                        dataSets.append(data)
                        recordCounter += len(data)
                    else:
                        if (len(data)+recordCounter) <= maximum:
                            dataSets.append(data)
                            recordCounter += len(data)
                        else:
                            dataSets.append(data.head(maximum-(len(data)+recordCounter)))
                            recordCounter += maximum-(len(data)+recordCounter)
                            break                                  
                else:
                    break                   
            else:
                raise Exception("unexpected response, no data") 
            if recordCounter>=totalRecords:
                break    
            page+=1
        if len(dataSets)>0:    
            return pd.concat(dataSets, sort=False)
        else:
            return pd.DataFrame()
                       
                                    
    
    def show(self, fields=None, size=None):   
        """
        Create a browseable representation of the items.
        
        Parameters
        ----------
        fields: list, optional
            A list of fields to limit the number of columns in the result
        size: integer, optional
            The number of items to show on each page when browsing the result
        """            
        #data
        data = widgets.Output()  
        if size is None:
            size = self.__records  
        self._set_page(self.__page, size)                               
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
                self._set_page(self.__page-1, size) 
                set_header_and_buttons(self.__page) 
                with data:
                    clear_output();
                    if not(fields==None):
                        rawData = self._filter_page(self.__data)
                        intersectList = [x for x in fields if x in rawData.columns.values]
                        dropList = [x for x in rawData.columns.values if x not in intersectList]
                        display(rawData.drop(columns=dropList)[intersectList])
                    else:    
                        display(self._filter_page(self.__data)) 
                
        def on_button_next(b):
            if self.__page<(self.__pages-1):
                set_header_and_buttons(self.__page+1) 
                button_previous.disabled=True
                button_next.disabled=True
                self._set_page(self.__page+1, size) 
                set_header_and_buttons(self.__page) 
                with data:
                    clear_output();
                    if not(fields==None):
                        rawData = self._filter_page(self.__data)
                        intersectList = [x for x in fields if x in rawData.columns.values]
                        dropList = [x for x in rawData.columns.values if x not in intersectList]
                        display(rawData.drop(columns=dropList)[intersectList])
                    else:    
                        display(self._filter_page(self.__data)) 
                
                
        set_header_and_buttons(self.__page)    
        with data:
            if not(fields==None):
                rawData = self._filter_page(self.__data)
                intersectList = [x for x in fields if x in rawData.columns.values]
                dropList = [x for x in rawData.columns.values if x not in intersectList]
                display(rawData.drop(columns=dropList)[intersectList])
            else:    
                display(self._filter_page(self.__data)) 
                  
        button_previous.on_click(on_button_previous)
        button_next.on_click(on_button_next)
        
        
        
        
        
        
        