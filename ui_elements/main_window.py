from IPython.external.qt_for_kernel import QtCore
from PyQt6.QtCore import QDateTime
from .ui_templates.main_window_template import Ui_MainWindow
from PyQt6.QtWidgets import QWidget
from .ui_templates.tax_row_template import Ui_tax_row
from .business_info import Business_info
from .clients_info import Clients_info
from .invoice_info import Invoice_info
from .data_models import Invoice_data_model
from PyQt6.QtWidgets import QMainWindow

class Tax_row (QWidget):
    def __init__(self,idx,parent,amount=None) -> None:
        super().__init__()
        self.idx=idx
        self.ui=Ui_tax_row()
        self.ui.setupUi(self)
        self.paernt=parent
        self.amount=amount
        self.rate=None

    def remove(self):
        self.paernt.removeWidget(self)

    def get_tax_info(self):
        if self.ui.tax_name.text() != "":
            return self.ui.tax_name.text,self.ui.tax_percentage.value()
        return None

    def calculate_tax(self):
        if self.amount is not None and self.rate is not None:
            return self.amount*(self.rate/100)
        return None

    def rate_changed(self,rate):
        print("rate_change")
        if rate!=self.rate:
            self.rate=rate
            tax=self.calculate_tax()
            if tax is not None:
                self.ui.tax_calc.setText(str(tax))

    def set_amount(self,amount):
        if amount !=self.amount:
            self.amount=amount
            tax=self.calculate_tax()
            if tax is not None:
                self.ui.tax_calc.setText(str(tax))

    def get_tax_result(self):
        print(f"tax name:{self.ui.tax_name.text()}")
        if self.ui.tax_name.text() != "" and self.amount is not None and self.rate is not None:
            return self.ui.tax_name.text(),self.calculate_tax()



class Main_widow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.business_info=Business_info("Business info")
        self.clients_info=Clients_info()
        self.invoice_info=Invoice_info(self)
        self.ui.actors_info.addWidget(self.business_info)
        self.ui.actors_info.addWidget(self.clients_info)
        self.ui.invoice_info.addWidget(self.invoice_info)
        self.total_ht=None
        self.set_preliminary_values()

    def set_preliminary_values(self):
        self.ui.due_date.setDate(QDateTime.currentDateTime().date())
        self.ui.creation_date.setDate(QDateTime.currentDateTime().date())
        self.ui.invoice_year.setValue(int(str(QDateTime.currentDateTime().date().year())[2:]))

    def gather_invoice_info(self):
        ui=self.ui
        res={
            "ref":f"{ui.invoice_number.value()}/{ui.invoice_year.value()}",
            "date":ui.creation_date.date().toString("dd/MM/yyyy"),
            "due_date":ui.due_date.date().toString("dd/MM/yyyy"),
            "project_name":ui.project_name.text()
        }
        return res

    def gather_tax_info(self):
        res=[]
        for idx in range(self.ui.tax_rows.count()):
            tax=self.ui.tax_rows.itemAt(idx).widget()
            tax_res=tax.get_tax_result()
            if tax_res is not None:
                name,value=tax_res
                res.append((name,value))

        return res

    def calculate_tax(self):
        amount= float(self.ui.total_ht.text()) if self.ui.total_ht.text()!="" else None
        for idx in range(self.ui.tax_rows.count()):
            self.ui.tax_rows.itemAt(idx).widget().set_amount(amount)

    def set_total(self,total):
        self.total_ht=total
        self.ui.total_ht.setText(str(total))

    def create_tax_row(self):
        amount= float(self.ui.total_ht.text()) if self.ui.total_ht.text()!="" else None
        self.ui.tax_rows.addWidget(Tax_row(0,self.ui.tax_rows,amount))

    def generate(self):
        invoice_info=Invoice_data_model()
        invoice_info.push_business_info(self.business_info.get_data())
        invoice_info.push_client_info(self.clients_info.get_data())
        a=self.gather_invoice_info()
        taxes=self.gather_tax_info()
        a["amount"]=self.total_ht+sum([tax[1]  for tax in taxes])
        invoice_info.push_invoice_info(a)
        invoice_info.push_items_info(self.invoice_info.get_data())
        invoice_info.push_tax_info([("Total HT",self.total_ht)]+self.gather_tax_info())

        print(invoice_info)
        invoice_info.generate(
            r"C:\Users\pc\Documents\programming\personal_projects\invoice_creator\templates\snippets.json",
            r"C:\Users\pc\Documents\programming\personal_projects\invoice_creator\templates\main.tex",
            r"C:/Users/pc/Documents/programming/personal_projects/invoice_creator/templates/logoSmaller.png",
            r"C:/Users/pc/Documents/programming/personal_projects/invoice_creator/templates"
        )
        print("generate")
