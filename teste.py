# import sys
# from PyQt5.QtWidgets import QApplication
# from PyQt5.Core import QUrl
# from PyQt5.QtWebkit import QWebPage
# import urllib1 , urllib2

from bs4 import BeautifulSoup
import csv
import requests
import pandas as pd
import time
from time import gmtime, strftime
date=strftime(" %d %b %Y", gmtime())
Tabela=[]
cancelado=0
#incerteza se faz alguma coisa
if cancelado==1:
    url="https://www.impic.pt/impic/pt-pt/consultar/empresas-com-licenca-ou-registo-suspenso-ou-cancelado-ha-menos-de-um-ano"
    id_type=str(27)
    name="cancelados"
if cancelado==0:
    url="http://www.impic.pt/impic/pt-pt/consultar/empresas-titulares-de-licenca-de-mediacao-imobiliaria"
    id_type=str(25)
    name="licenças_ativas"
#Tabela
id_type=str(8)


#Paginas
pag_inicial=1
pag_final=438
#cookie
PHPSESSID='60cdpo8cih3roqn22968jai2s5'
def Table(x,y,url=url): 

    cookies = {
        'PHPSESSID': PHPSESSID,
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8,pt-PT;q=0.5,pt;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://www.impic.pt',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': url,
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    
    data = {
      'id_type': '8',
      'id_object': id_type,
      'pesquisar': 'true',
      'loadTable': '{}'.format(x),
          'pageSearch': '{}'.format(y)
    }

    r = requests.post('https://www.impic.pt/impic/ajax/call/impic_api/consultar/ajax/43', headers=headers, data=data,cookies=cookies)
    #r = requests.post('https://www.impic.pt/impic/ajax/call/impic_api/consultar/ajax/43', headers=headers, cookies=cookies, data=data,verify=False)
    
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

# Numero_Paginas=[]
# Numero_Paginas=[int(item) for item in input("Escreva a começar e o numero a acabar ex:(1,2)(1,357):    ").split()]

for i in range(pag_inicial,pag_final+1):
    Table(1,i)
    #time.sleep(1)
    print("paginas feita: "+str(i))
    
teste=Tabela    
df=pd.DataFrame(teste)

#to excell
#df.to_excel("Impic.xlsx")  
df.to_excel("C:/Users/joaot/Desktop/Codigo/IMPIC project/IMPIC_{}_{}.xlsx".format(name,date)) 

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