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
name='empresas-titulares-de-licenca-de-mediacao-imobiliaria'
Tabela=[]
def table(x,y):  
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
        'Referer': 'http://www.impic.pt/impic/pt-pt/consultar/{}'.format(name),
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    
    data = {
      'id_type': '8',
      'id_object': '25',
      'pesquisar': 'true',
      'loadTable': '{}'.format(x),
          'pageSearch': '{}'.format(y)
    }
    
    r = requests.post('http://www.impic.pt/impic/ajax/call/impic_api/consultar/ajax/43', headers=headers, cookies=cookies, data=data)
    
    content=(r.text)

    soup = BeautifulSoup(content, "html5lib")
    
    
    table=soup.table
    table_row= table.find_all("tr")

    for tr  in table_row:
        td = tr.find_all("td")
        row = [i.text for i in td]
        Tabela.append(row)
        
# Numero_Paginas=[]
# Numero_Paginas=[int(item) for item in input("Escreva a começar e o numero a acabar ex:(1,2)(1,357):    ").split()]

for i in range(1,439):
    table(1,i)
    print(i,"/439")
teste=Tabela    
df=pd.DataFrame(teste)

df.to_excel("{}.xlsx".format(name))  


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