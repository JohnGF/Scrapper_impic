# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 13:49:35 2020

@author: John
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def fetch_page(x, y, name, timeout=10):
    """Fetches a page of data from the API."""
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
    
    r = requests.post(
        'http://www.impic.pt/impic/ajax/call/impic_api/consultar/ajax/43',
        headers=headers,
        cookies=cookies,
        data=data,
        timeout=timeout
    )
    r.raise_for_status()
    return r.text

def extract_table(html_content):
    """Extracts rows from an HTML table."""
    soup = BeautifulSoup(html_content, "html5lib")
    table = soup.table
    
    if not table:
        return []
        
    table_row = table.find_all("tr")
    extracted_rows = []
    
    for tr in table_row:
        td = tr.find_all(["td", "th"])
        if not td:
            continue
        row = [i.text.strip() for i in td]
        extracted_rows.append(row)
        
    return extracted_rows

def extract_license(text):
    """Extracts a license number from text using regex."""
    # Example regex pattern for license numbers like 12345-AMI
    pattern = r'(\d+-AMI)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

def export_data(data, filename):
    """Exports data to an Excel file."""
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def main():
    name = 'empresas-titulares-de-licenca-de-mediacao-imobiliaria'
    Tabela = []
    
    for i in range(1, 439):
        try:
            print(f"{i}/439")
            html_content = fetch_page(1, i, name)
            rows = extract_table(html_content)
            Tabela.extend(rows)
        except Exception as e:
            print(f"Error fetching page {i}: {e}")
            
    export_data(Tabela, f"{name}.xlsx")
    print(f"Exported to {name}.xlsx")

if __name__ == "__main__":
    main()
