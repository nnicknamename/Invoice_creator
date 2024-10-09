import re
from latexcompiler import LC
import os
import json
import pandas as pd
from pathlib import Path

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


class Invoice_filler():
    tags={
        "tax_rate":"#TAX_RATE",
        "invoice_ref":"#INVOICE_REF",
        "due_time":"#DUE_TIME",
        "project_name":"#PROJECT_NAME",
        "logo_path":"#LOGO_PATH",
        "company_info":"#COMPANY_INFO",
        "client_info":"#CLIENT_INFO",
        "terms_conditions":"#TERMS_CONDITIONS",
        "invoice_items":"#INVOICE_ITEMS"
    }
    def __init__(self,
                 template_snippets_path:str,
                 template_path:str,
                 company_info:dict,
                 client_info:dict,
                 tax_info:dict,
                 logo_path:str,
                 terms_conditions:str) -> None:
        self.tempalte=load_text(template_path)
        self.company_info=company_info
        self.client_info=client_info
        self.tax_info=tax_info
        self.logo_path=logo_path
        self.terms_conditions=terms_conditions
        self.template_snippets=load_json(template_snippets_path)

    def _render_invoice_items(self,invoice_data):
        """
            Creates partial tex code for the given invoice data.
        """
        res=""
        for task in invoice_data:
            t=task
            for item in invoice_data[task]:
                snippet=r"\\"+self.template_snippets["items"]["item"]
                snippet=self._fill_snippet("#1",t,snippet)
                snippet=self._fill_snippet("#2",invoice_data[task][item]["detail"],snippet)
                snippet=self._fill_snippet("#3",invoice_data[task][item]["qt"],snippet)
                snippet=self._fill_snippet("#4",invoice_data[task][item]["price"],snippet)
                snippet=self._fill_snippet("#4",invoice_data[task][item]["total"],snippet)
                t=r""
                res+=snippet+"\n"
            res+=r"\\"+self.template_snippets["items"]["separator"]+"\n"
        # print(res)
        return res

    def _render_business_info(self,business_info:dict,actor_type:str)->str:
        """
        """
        res=""
        for key in business_info:
            snippet=r"\\"+self.template_snippets[actor_type][key]
            snippet=self._fill_snippet("#",business_info[key],snippet)
            res+=snippet
        print(res)
        return res

    def _fill_snippet(self,search,data,snippet,prefix=""):
        a=re.sub(search,f"{prefix}{data}",snippet)
        return a

    def _fill_template(self,ref:str,due_time:int,project_name:str,invoice_data:dict)->str:
        """
        """
        res=self.tempalte
        # res=self._fill_snippet(self.tags["tax_rate"],self.tax_rate,res)
        res=self._fill_snippet(self.tags["invoice_ref"],ref,res)
        res=self._fill_snippet(self.tags["due_time"],str(due_time),res)
        res=self._fill_snippet(self.tags["project_name"],project_name,res)
        res=self._fill_snippet(self.tags["logo_path"],self.logo_path,res)
        res=self._fill_snippet(self.tags["company_info"],self._render_business_info(self.company_info,"company"),res)
        res=self._fill_snippet(self.tags["client_info"],self._render_business_info(self.client_info,"client"),res)
        res=self._fill_snippet(self.tags["terms_conditions"],self.terms_conditions,res)
        res=self._fill_snippet(self.tags["invoice_items"],self._render_invoice_items(invoice_data),res)
        return res

    def _save_latex(self,render_path,filled_template):
        doc_path=render_path+"/temp.tex"
        with open(doc_path,"w") as file:
            file.write(filled_template)
        return doc_path

    def compile_document(self,render_path):
        path=os.path.abspath(render_path)

        LC.compile_document(tex_engine="pdflatex",
                            bib_engine='biber',
                            no_bib=True,
                            path=path,
                            folder_name=Path(path).parent)
    
    def render_document(self,ref:str,due_time:int,project_name:str,invoice_data:dict,render_dir:str):
        filled_template=self._fill_template(ref,due_time,project_name,invoice_data)
        doc_path=self._save_latex(render_dir,filled_template)
        self.compile_document(doc_path)


if __name__=="__main__":
    templates_path=r"./templates/"
    company_info=load_csv(r"./company_info.csv")
    client_info={
        "NAME":"skycam",
        "ADRESS":"adrSkycam",
        "TEL":"012384723",
        "RC":"r12398410239",
        "NIF":"n12934810239",
        "AI":"a123948129",
        "RIB":"r12984710239"
    }
    filler=Invoice_filler(r"./templates/snippets.json",
                          r"./templates/main.tex",
                          company_info,
                          client_info,
                          {"test tax":199,"one":121},
                          r"logoSmaller.png",
                          "nothing")

    invoice_data={
        "Roto":{
            "firstTask":{"qt":10,"price":10000},
            "secondTask":{"qt":10,"price":10000},
            "thirdTask":{"qt":10,"price":10000}
        },
        "Stuff":{
            "stuffTask":{"qt":1,"price":10000}
        }
    }
    filler.render_document("001",
                           due_time=90,
                           project_name="VFX",
                           invoice_data=invoice_data,
                           render_dir=r"./templates/")


