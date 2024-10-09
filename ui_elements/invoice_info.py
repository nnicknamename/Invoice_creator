
from .ui_templates.invoice_info_template import Ui_Invoice_info_template
from PyQt6.QtWidgets import QHeaderView,QWidget
from PyQt6 import QtWidgets
from .data_models import Itemlist_data_model
from .utils import file_dialog
import os
import pandas as pd



class Invoice_info(QWidget):
    def __init__(self,main_window) -> None:
        super().__init__()
        self.ui=Ui_Invoice_info_template()
        self.ui.setupUi(self)
        self.data_model=None
        self.main_window=main_window
        # self.ui.label_2.setText("Invoice info")

    def _table_setup(self,table):
        table.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(True)
        table.horizontalHeader().setVisible(True)

    def _load_table_data(self,table,data_path:str):
        format=os.path.splitext(data_path)[-1]
        assert format in [".json",".csv"],"file format not supported"
        print(f"format {format}")
        if format==".json":
            data=pd.read_json(data_path,orient="index").reset_index()
        elif format==".csv":
            print("reading csv")
            data=pd.read_csv(data_path)
        else:
            return None
        dm=Itemlist_data_model(data,data_path,self)
        table.setModel(dm)
        return dm


    def get_data(self):
        if self.data_model is not None:
            return self.data_model.get_data()

    def load(self):
        files=file_dialog(self,f"open invoice info file","Data files (*.csv *.json)")
        if  isinstance(files,list):
            data_model=self._load_table_data(self.ui.info_table,files[0])

            self._table_setup(self.ui.info_table)
            self.data_model=data_model

    def delete_selected(self):
        if self.data_model is not None:
            self.data_model.delete_rows(self.ui.info_table.selectionModel().selectedRows())
            self.update()
    
    def add_row(self):
        if self.data_model is not None:
            selection=self.ui.info_table.selectionModel().selectedRows()
            below= not QtWidgets.QApplication.keyboardModifiers()
            self.data_model.add_row([r.row() for r in selection],below)
            self.update()

    def update_total(self,total):
        self.main_window.set_total(total)

    def save(self):
        if self.data_model is not None:
            self.data_model.save()


