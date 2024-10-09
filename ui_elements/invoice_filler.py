import re
from latexcompiler import LC
import os
from pathlib import Path
import json
def load_json(path):
    with open(path,"r") as file:
        dict=json.load(file)
    return dict

def load_text(path):
    with open(path,"r") as file:
        template="".join(file.readlines())
    return template

class Invoice_filler():
    tags={
        "tax_rate":"#TAX_RATE",
        "invoice_ref":"#INVOICE_REF",
        "date":"#DATE",
        "due_date":"#DUE_DATE",
        "project_name":"#PROJECT_NAME",
        "logo_path":"#LOGO_PATH",
        "company_info":"#COMPANY_INFO",
        "client_info":"#CLIENT_INFO",
        "terms_conditions":"#TERMS_CONDITIONS",
        "invoice_items":"#INVOICE_ITEMS",
        "amount":"#AMOUNT"
    }
    def __init__(self,
                 template_snippets_path:str,
                 template_path:str,
                 company_info:dict,
                 client_info:dict,
                 tax_info:dict,
                 invoice_info:dict,
                 logo_path:str,
                 terms_conditions:str) -> None:
        self.tempalte=load_text(template_path)
        self.company_info=company_info
        self.client_info=client_info
        self.tax_info=tax_info
        self.logo_path=logo_path
        self.invoice_info=invoice_info
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
                snippet=self._fill_snippet("#2",item["detail"],snippet)
                snippet=self._fill_snippet("#3",item["qt"],snippet)
                snippet=self._fill_snippet("#4",item["unit"],snippet)
                snippet=self._fill_snippet("#5",item["total"],snippet)
                t=r""
                res+=snippet+"\n"
            res+=r"\\"+self.template_snippets["items"]["separator"]+"\n"
        res+=fr"\\{self.template_snippets['items']['starttax']}"+"\n"

        for tax in self.tax_info:
            snippet=r"\\"+self.template_snippets["items"]["tax_item"]
            snippet=self._fill_snippet("#1",tax[0],snippet)
            snippet=self._fill_snippet("#2",tax[1],snippet)
            res+=snippet+"\n"
        print(res)
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

    def _fill_template(self,invoice_data:dict)->str:
        """
        """
        res=self.tempalte
        res=self._fill_snippet(self.tags["invoice_ref"],self.invoice_info['ref'],res)
        res=self._fill_snippet(self.tags["due_date"],str(self.invoice_info["due_date"]),res)
        res=self._fill_snippet(self.tags["date"],str(self.invoice_info["date"]),res)
        res=self._fill_snippet(self.tags["project_name"],self.invoice_info["project_name"],res)
        res=self._fill_snippet(self.tags["logo_path"],self.logo_path,res)
        res=self._fill_snippet(self.tags["company_info"],self._render_business_info(self.company_info,"company"),res)
        res=self._fill_snippet(self.tags["client_info"],self._render_business_info(self.client_info,"client"),res)
        res=self._fill_snippet(self.tags["terms_conditions"],self.terms_conditions,res)
        res=self._fill_snippet(self.tags["invoice_items"],self._render_invoice_items(invoice_data),res)
        res=self._fill_snippet(self.tags["amount"],self.invoice_info["amount"],res)
        return res

    def _save_latex(self,render_path,filled_template):
        doc_path=render_path+"/temp.tex"
        with open(doc_path,"w") as file:
            file.write(filled_template)
        return doc_path

    def compile_document(self,render_path):
        path=os.path.abspath(render_path)
        print("path: ",path)
        print ("parent: ",Path(path).parent)
        LC.compile_document(tex_engine="pdflatex",
                            bib_engine='biber',
                            no_bib=True,
                            path=path,
                            folder_name=str(Path(path).parent))

    def render_document(self,invoice_data:dict,render_dir:str):
        filled_template=self._fill_template(invoice_data)
        doc_path=self._save_latex(render_dir,filled_template)
        self.compile_document(doc_path)
