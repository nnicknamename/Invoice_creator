from .ui_templates.clients_info_template import Ui_clients_info
from PyQt6.QtWidgets import QHeaderView,QWidget,QMessageBox
from PyQt6 import QtWidgets
from .data_models import Clients_data_model
from .utils import file_dialog,read_data_file

class Clients_info(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui=Ui_clients_info()
        self.ui.setupUi(self)
        self.data_model=None
        self.ui.search_box.completer().setCompletionMode(QtWidgets.QCompleter.CompletionMode.PopupCompletion)

    def _load_table_data(self,data_path:str):
        data=read_data_file(data_path)
        if data is None or not Clients_data_model.validate(data):
            return None
        wordlist = data["NAME"]
        self.ui.search_box.addItems(wordlist)
        dm=Clients_data_model(data,0,data_path)
        self.ui.info_table.setModel(dm)
        return dm

    def selection_changed(self,idx):
        print(f"selected{idx}")
        if self.data_model is not None:
            self.data_model.show_row(idx)
            self.ui.info_table.update() 

    def load(self):
        files=file_dialog(self,f"open Clients info file","Data files (*.csv *.json)")
        if  isinstance(files,list):

            data_model=self._load_table_data(files[0])
            if data_model is None:
                QMessageBox.critical(self,"File error","The provided Client's data file is not valid.")
            else:
                self._table_setup(self.ui.info_table)

    def get_data(self):
        if self.data_model is not None:
            dataa=self.data_model.get_data()
            assert dataa.shape==(7,2)
            return {row.iloc[0]:row.iloc[1]  for _,row in dataa.iterrows()}

    def save(self):
        if self.data_model is not None:
            self.data_model.save()

    def _table_setup(self,table):
        table.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)

