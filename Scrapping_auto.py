# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 13:49:35 2020

@author: John
"""
# import sys
# from PyQt5.QtWidgets import QApplication
# from PyQt5.Core import QUrl
# from PyQt5.QtWebkit import QWebPage
# import urllib1 , urllib2

from bs4 import BeautifulSoup
import csv
import requests
import pandas as pd
from time import gmtime, strftime
date=strftime(" %d %b %Y", gmtime())
page = requests.get("http://www.impic.pt/impic/pt-pt/consultar/empresas-titulares-de-licenca-de-mediacao-imobiliaria")
soup = BeautifulSoup(page.content, "html.parser")
result=soup.find("a",string="Mediação Imobiliária")
links=result.parent.children
tabela=[i for i in links]
ul=[]
href=[]
name=[]
Id=[]
payload=tabela[3].find_all("a")
for i in payload:
    href.append(i["href"])
    Id.append(i["id"][7::])
    name.append(i.text)



Tabela=[]
def table(x,y,referer,ID):  
    cookies = {
        'PHPSESSID': '55kpb8ce7nrvhrlj2nnjmepdb3',
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8,pt-PT;q=0.5,pt;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://www.impic.pt',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': '{}'.format(referer),
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    
    data = {
      'id_type': '8',
      'id_object':'{}'.format(ID),
      'pesquisar': 'true',
      'loadTable': '{}'.format(x),
          'pageSearch': '{}'.format(y)
    }

    r = requests.post('http://www.impic.pt/impic/ajax/call/impic_api/consultar/ajax/43', headers=headers, cookies=cookies, data=data)
    
    if r.content==b'':
        return 0
    content=(r.text)

    soup = BeautifulSoup(content, "html5lib")

    table_var=soup.table
    if table_var==None:
        return 0
    table_row= table_var.find_all("tr")

    for tr  in table_row:
        td = tr.find_all("td")
        row = [i.text for i in td]
        Tabela.append(row)
    return r   
# Numero_Paginas=[]
# Numero_Paginas=[int(item) for item in input("Escreva a começar e o numero a acabar ex:(1,2)(1,357):    ").split()]

del(name[1])
del(name[1])
del(name[2]) 
for i in range(len(name)):
    #carregar modo tabela ou nao 1/0
    x=1
    referer=href[i]
    ID=Id[i]
    for y in range(1,450):
        print(y,"/450")
        T=table(x,y,referer,ID)
    if T==0:
        break
    teste=Tabela    
    df=pd.DataFrame(teste)
    df=df.dropna(thresh=3)
    #df=df.join(df[3].str.split("  +",expand=True),how="right",lsuffix="a",rsuffix="b")
    #df.pop('3a')

    df.to_excel("{}_{}.xlsx".format(name[i],date),index=False)     

# with open("test1.csv","a",newline="") as fp:
#     a = csv.writer(fp,delimeter=",")
#     a.writerows(Tabela)
#     for row in a:
#         stop=0


# 

# if 
# request =requests.get("http://www.impic.pt/impic//pt-pt/consultar/empresas-titulares-de-alvara-de-empreiteiro-de-obras-publicas")
# soup = bs.BeautifulStoneSoup(request.content)

# class Client(QWebPage):
#     def _init_ (self,url):
#         self.app = QApplication(sys.argv)
#         self.loadFinished.connect(self.on_page_load)
#         self.mainFrame().load(QUrl(url))
#         self.app.exec_()
#     def on_page_load(self):
#         self.app.quit()
# url = "http://www.impic.pt/impic//pt-pt/consultar/empresas-titulares-de-alvara-de-empreiteiro-de-obras-publicas"
# client_response=Client(url)
# source= client_response.mainFrame().toHtml()

# # source = urllib.request.urlopen("http://www.impic.pt/impic//pt-pt/consultar/empresas-titulares-de-alvara-de-empreiteiro-de-obras-publicas")
# soup=bs.BeautifulStoneSoup(source, "lxml")
# js_test = soup.find("p", class_="jstest")
# print(js_test.txt)