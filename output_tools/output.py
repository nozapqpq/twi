# coding: utf-8
import os
import re
import json

class Output():
    def __init__(self):
        i = 0

    def json_import(self, json_fn):
        f = open(json_fn,'r')
        return json.load(f)

    def json_export(self, json_fn, output_dict):
        f = open(json_fn,'w')
        json.dump(output_dict,f)

    # 要改良？
    def write_list_to_csv(self,filename,target):
        with open(filename,'w') as f:    
            writer = csv.writer(f)       
            writer.writerow(["a","b","c"])
            for a in target:             
                writer.writerow(a)       
    def write_list_to_csv_nest(self,filename,target):
        with open(filename,'w') as f:    
            writer = csv.writer(f)       
            writer.writerow(["a","b","c"])
            for a in target:             
                for b in a:              
                    writer.writerow(b)
