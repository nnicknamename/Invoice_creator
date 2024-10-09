import regex as re
from latexcompiler import LC
import json
from jinja2 import Environment, FileSystemLoader
import pandas as pd 
class Invoice():
    def __init__(self,project:Project,client_info:dict,company_info:dict,template_path) -> None:
        self.emplate_path=template_path
        self.template=self.read_template(template_folder)
        self.invoice=self.fill_info(company_info,self.template)
        self.invoice=self.fill_info(client_info,self.invoice)
        self.invoice=self.fill_invoice_items(project,self.invoice)
        self.generate_latex()

    def fill_invoice_items(self,project:Project,template:str):
        res=''+template
        res=re.sub('#ProjectName#',project['ProjectName'],res)
        res=re.sub('#InvoiceNum#',str(project['ProjectNum']),res)
        sub_projects_latex=""
        for sub_project in project["Sub_projects"]:
            sub_projects_latex+="\invoiceitem{"+sub_project["Name"]+"}{"+str(sub_project["Quantity"])+"}{"+str(sub_project["UnitPrice"])+"}\n"
        res=re.sub('#Invoice#',sub_projects_latex,res)
        return res
    
    def fill_info(self,company_info:dict,template:str):
        res=""+template
        for key in company_info.keys():
            res=re.sub("#"+key+"#",str(company_info[key]),res)
        return res
    
    def read_template(self,path):
        with open(path+"/main.ttemp", 'r') as file:
            data=file.read()
        return data
    
    def generate_latex(self):
        with open(self.template_folder+"/main.tex","w") as file:
            file.write(self.invoice)
    
    def compile(self):
            LC.compile_document(tex_engine="pdflatex",
                                bib_engine='biber',
                                no_bib=True,
                                path=self.template_path,
                                folder_name=self.template_folder)


class Invoice_01():
    def __init__(self,csv_path) -> None:
        self.environment = Environment(loader=FileSystemLoader("templates/"))
        self.data=pd.read_csv(csv_path)

    def _fill_template(self,data):
        pass

if __name__=="__main__":
    clientInfo=Client("shit client .inc",email="shit.inc@gmail.com",phoneNumber="696969",address="shit town")

    with open('Company_info.json', 'r') as file:
        companyInfo=json.load(file)

    project=Project(name="first project",number=1,brand="shit brand .inc",negotiation=7)
    project.add_sub_project(Sub_project("Turd 3D",quantity=10,ptype="Modeling",price=1000,deadline=datetime.datetime(2023,10,10)))
    project.add_sub_project(Sub_project("fish",quantity=1,ptype="Modeling",price=5000,deadline=datetime.datetime(2023,10,12)))
    print(project)

    invoice=Invoice(template_folder=r"C:\Users\pc\Documents\programming\3D_Modeling_Database\Invoice_template",client_info=clientInfo,company_info=companyInfo,project=project)
    invoice.compile()



#InvoiceNum#
#projectName#
    #ClientName#
        #ClientJob#
    #ClientAddress#
        #ClientAddress1#
    #ClientEmail#
    #ClientNumber#

    #CompanyName#
    #SenderName#
    #SenderJob#
    #SenderAddress#
    #SenderAddress1#
    #SenderEmail#
    #SenderNumber#

#TermsConditions#
#invoice#
