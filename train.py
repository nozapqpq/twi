# coding: utf-8
import os
import re
from machine_learning import model
from output_tools import output
import utility

def train():
    util = utility.Utility()
    output_tools = output.Output()
    model_name = util.get_deep_model_name(output_tools.json_import("settings.json")["settings"])
    import_list = output_tools.json_import(model_name+"_input.json")
    dl_input = import_list["input"]
    dl_output = import_list["output"]

    dl_model = model.model(dl_input, dl_output)
    dl_model.knn_train(import_list)
    dl_model.save(model_name)

if __name__ == "__main__":
    train()
