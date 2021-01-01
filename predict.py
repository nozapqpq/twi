# coding: utf-8
import os
import re

from machine_learning import model
from output_tools import output
import utility

def predict():
    util = utility.Utility()
    output_tools = output.Output()
    model_name = util.get_deep_model_name(output_tools.json_import("settings.json")["settings"])
    import_list = output.Output().json_import(model_name+"_input.json")
    dl_input = import_list["input"]
    dl_output = import_list["output"]

    dl_model = model.model()
    dl_model.load(model_name)
    predicted = dl_model.predict(dl_input).tolist()
    output_tools.json_export(model_name+"_predict.json",{"predict":predicted})

if __name__ == "__main__":
    predict()
