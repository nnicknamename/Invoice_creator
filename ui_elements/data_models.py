from num2words import num2words
import typing
from PyQt6.QtCore import QModelIndex,QVariant
from PyQt6.QtCore import QAbstractTableModel,Qt,QModelIndex
import pandas as pd
from .invoice_filler import Invoice_filler


class Actor_data_model(QAbstractTableModel):
    def __init__(self, data:pd.DataFrame):
        super().__init__()
        self._data = data

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self._data.shape[0]

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)

    def setData(self, index: QModelIndex, value: typing.Any, role: int = 0) -> bool:
        print(f"setting data role:{role}")
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            return True
        return False

    def flags(self, index):
        if index.column()==0:
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled 
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

class Clients_data_model(QAbstractTableModel):
    def __init__(self, data:pd.DataFrame,row,path):
        super().__init__()
        self._data = data
        self.path=path
        self.row=row
        self.data_changed=False
    
    @classmethod
    def validate(cls,data:pd.DataFrame):
        for c in data.columns:
            if not c in ["NAME","ADRESS","TEL","RC","NIF","AI","RIB"]:
                return False
        return True

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self._data.iloc[self.row].transpose().shape[0]

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 2

    def show_row(self,idx):
        self.row=idx


    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data.iloc[self.row].transpose().to_frame().reset_index().iloc[index.row(),index.column()]
                return str(value)

    def get_data(self):
        return self._data.iloc[self.row].transpose().to_frame().reset_index()

    def setData(self, index: QModelIndex, value: typing.Any, role: int = 0) -> bool:
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[self.row,index.row()] = value
            self.data_changed=True
            return True
        return False

    def save(self):
        if self.data_changed:
            self._data.to_csv(self.path,index=False)
            self.data_changed=False

    def flags(self, index):
        if index.column()==0:
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled 
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable


class Business_data_model(Actor_data_model):
    def __init__(self, data: pd.DataFrame,path):
        self.path=path
        super().__init__(data)

    @classmethod
    def validate(cls,data:pd.DataFrame):
        return data.columns.to_list()==["Field","value"]

    def save(self):
        self._data.to_csv(self.path,index=False)


# Calculated fields:
# the idea is to add a subset of columns that get updated when some functions gets called,
# the calculated fields can be stored in a different structure to keep the main data easily savable
#

class Itemlist_data_model(QAbstractTableModel):
    def __init__(self, data:pd.DataFrame,path:str,par):
        self.path=path
        self.par=par
        super().__init__()
        self._data = data
        self.price=[]
        self.calculate_prices()
        self.par.update_total(self.calculate_prices())

    def updates_total(f):
        def func(self,*args,**kwargs):
            res=f(self,*args,**kwargs)
            self.par.update_total(self.calculate_prices())
            return res
        return func

    def calculate_prices(self):
        return sum(self._data["unit"].astype(float)*self._data["qt"].astype(int))

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self._data.shape[0]

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self._data.shape[1]+1

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                if index.column()<self._data.shape[1]:
                    value = self._data.iloc[index.row(), index.column()]
                    return str(value)
                else:
                    value=float(self._data["unit"].iloc[index.row()])*int(self._data["qt"].iloc[index.row()])
                    return str(value)
    @updates_total
    def setData(self, index: QModelIndex, value: typing.Any, role: int = 0) -> bool:
        print(f"setting data role:{role}")
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            return True
        return False

    def flags(self, index):
        if index.column()<self._data.shape[1]:
        # if index.column()==0:
        #     return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled 
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
        else:
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled 

    def get_data(self):
        data=self._data.copy()
        data["total"]=data["unit"].astype(float)*data["qt"].astype(float)
        res={key:[]  for key in data.groupby("task").groups}

        for key in data.groupby("task").groups:
            items=data.groupby("task").get_group(key)
            for _,task in items.iterrows():
                res[key].append(task[task!="task"].drop("task").to_dict())
        return res

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if section <len(self._data.columns):
                    return self._data.columns[section]
                else:
                    return "price"
        return QVariant()

    @updates_total
    def delete_rows(self,selected_rows):
        if len(selected_rows)>0:
            self.beginRemoveRows(selected_rows[0],selected_rows[0].row(),selected_rows[-1].row())
            self._data.drop([r.row() for r in selected_rows],inplace=True)
            self._data.reset_index(drop=True,inplace=True)
            self.endRemoveRows()

    @updates_total
    def add_row(self,selection,below=True):
        self.beginInsertRows(QModelIndex(),0,0)
        if selection is None or len(selection)==0:
            self._data.loc[-1]=["","",0,0]
        else:
            if below:
                self._data.loc[selection[-1]+0.5]=["","",0,0]
            else:
                self._data.loc[selection[0]-0.5]=["","",0,0]
        self._data.sort_index(inplace=True)
        self._data.reset_index(drop=True,inplace=True)
        self.endInsertRows()


    def save(self):
        self._data.to_csv(self.path,index=False)

class Invoice_data_model():
    """
        An invoice data model is used to collect and verify all data gathered from ui elements
        data will be pushed to an Invoice_data_model and a boolean value will be returned, informing 
        the pushing element of the validity of its information, thus gives it a chace to inform the user.
        an Invoice_data_model by concequence is the final verifier of data integrity before the generation 
        of the invoice.
    """
    business_keys={"NAME","ADRESS","TEL","RC","NIF","AI","RIB"}
    invoice_info_keys={"ref","date","due_date","project_name","amount"}

    def __init__(self) -> None:
        self.clinet_info=None
        self.business_info=None
        self.invoice_info=None
        self.tax_info=None
        self.items_info=None

    def push_client_info(self,data:dict):
        assert set(data.keys())==self.business_keys
        self.clinet_info=data

    def push_business_info(self,data:dict):
        assert set(data.keys())==self.business_keys
        self.business_info=data

    def push_invoice_info(self,data:dict):
        assert set(data.keys())==self.invoice_info_keys
        self.invoice_info=data

    def push_items_info(self,data:dict):
        self.items_info=data

    def push_tax_info(self,data:dict):
        self.tax_info=data

    def generate(self,template_snippets_path:str,template_path:str,logo_path:str,render_dir:str):
        assert self.invoice_info is not None,"invoice info is required in order to generate an invoice"
        filler=Invoice_filler(
            template_snippets_path=template_snippets_path,
            template_path=template_path,
            company_info=self.business_info,
            client_info=self.clinet_info,
            tax_info=self.tax_info,
            invoice_info=self.invoice_info,
            logo_path=logo_path,
            terms_conditions=num2words(self.invoice_info["amount"],lang="fr")
        )
        filler.render_document(invoice_data=self.items_info,
                               render_dir=render_dir
                               )

    def __str__(self) -> str:
        return f"""
Invoice_data:
    - Business_info:
        {self.business_info.__str__()}
    - Client_info:
        {self.clinet_info.__str__()}
    - Invoice_info:
        {self.invoice_info.__str__()}
    - Items_info:
        {self.items_info.__str__()}
    - Tax_info:
        {self.tax_info.__str__()}
        """
