from ui_elements.ui_templates.actor_info_template import Ui_Form
from .data_models import  Business_data_model
from .utils import *
from PyQt6.QtWidgets import QHeaderView,QWidget,QErrorMessage
from PyQt6


class Business_info(QWidget):
    def __init__(self,actor_name) -> None:
        super().__init__()
        self.actor_name=actor_name
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        self.ui.label_2.setText(actor_name)
        self.data_model=None

    def _table_set_look(self,table):
        table.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)

    def _load_table_data(self,table,data_path:str):
        data=read_data_file(data_path)
        if data is None:
            return None
        dm=Business_data_model(data,data_path)
        table.setModel(dm)
        return dm

    def get_data(self):
        if self.data_model is not None:
            assert self.data_model._data.shape==(7,2)
            return {row.iloc[0]:row.iloc[1]  for a,row in self.data_model._data.iterrows()}

    def load(self):
        files=file_dialog(self,f"open {self.actor_name} info file","Data files (*.csv *.json)")
        if isinstance(files,list):
            data_model=self._load_table_data(self.ui.info_table,files[0])
            if data_model is None:
                QErrorMessage(self).showMessage("The provided file is not a valid Business info file.")
            else:
                self.data_model=data_model
            self._table_set_look(self.ui.info_table)

    def save(self):
        if self.data_model is not None:
            self.data_model.save()


