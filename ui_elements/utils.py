from PyQt6.QtWidgets import QFileDialog
import os
import json
import pandas as pd

def load_json(path):
    with open(path,"r") as file:
        dict=json.load(file)
    return dict

def load_csv(path):
    df=pd.read_csv(path)
    return {row["Field"]:row["value"]  for row in df.to_dict("records")}

def load_text(path):
    with open(path,"r") as file:
        template="".join(file.readlines())
    return template

def read_data_file(data_path:str)->pd.DataFrame|None:
    format=os.path.splitext(data_path)[-1]
    assert format in [".json",".csv"],"file format not supported"
    data=None
    if format==".json":
        data=pd.read_json(data_path,orient="index").reset_index()
    elif format==".csv":
        print("reading csv")
        data=pd.read_csv(data_path)
    return data

def file_dialog(parent,message,file_filter):
    dialog= QFileDialog(parent, message)
    dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
    dialog.setNameFilters([file_filter])
    if dialog.exec():
        filenames = dialog.selectedFiles()
        return filenames
