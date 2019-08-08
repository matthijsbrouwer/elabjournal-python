from .eLABJournalObject import * 

import json
import pandas as pd
import numbers

class SampleSerie(eLABJournalObject):

    def __init__(self, api, data):        
        """
        Internal use only: initialize sample serie
        """
        if ((data is not None) & (type(data) == dict) & 
            ("name" in data.keys())
           ):
            super().__init__(api, data, "seriesID", str(data["name"])) 
        else:
            raise Exception("no (valid) sampleSerie data") 
        
    def barcode(self):
        """
        Get the barcode.
        """
        if "barcode" in self.data():
            barcode = self.data()["barcode"]
            return(barcode)
        return None
        
    def samples(self):
        """
        Get a dict with the samples for this sample serie.
        The sampleID is used as a key, the value is a sample object.                
        """
        sample_list = []
        if "samples" in self.data():
            samplesData = self.data()["samples"]
            if isinstance(samplesData, list):
                for sampleItem in samplesData:
                    if isinstance(sampleItem,dict) & ("sampleID" in sampleItem):
                        sample_list.append(sampleItem["sampleID"])
                    elif isinstance(sampleItem,numbers.Integral) | isinstance(sampleItem,str):
                        sample_list.append(sampleItem)
        return(self._eLABJournalObject__api.sample(sample_list))
    
    