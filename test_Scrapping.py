import pytest
import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

from Scrapping import fetch_page, extract_table, extract_license, export_data

def test_fetch_page_success(requests_mock):
    """Test successful page fetch."""
    url = 'http://www.impic.pt/impic/ajax/call/impic_api/consultar/ajax/43'
    expected_html = '<table><tr><td>Test Data</td></tr></table>'
    requests_mock.post(url, text=expected_html)
    
    result = fetch_page(1, 1, 'test-name')
    assert result == expected_html

def test_fetch_page_timeout(requests_mock):
    """Test page fetch timeout."""
    url = 'http://www.impic.pt/impic/ajax/call/impic_api/consultar/ajax/43'
    requests_mock.post(url, exc=requests.exceptions.Timeout)
    
    with pytest.raises(requests.exceptions.Timeout):
        fetch_page(1, 1, 'test-name', timeout=1)

def test_extract_table_valid_html():
    """Test extracting table from valid HTML."""
    html = '''
    <table>
        <tr><th>Header 1</th><th>Header 2</th></tr>
        <tr><td>Data 1</td><td>Data 2</td></tr>
        <tr><td>Data 3</td><td>Data 4</td></tr>
    </table>
    '''
    expected = [
        ['Header 1', 'Header 2'],
        ['Data 1', 'Data 2'],
        ['Data 3', 'Data 4']
    ]
    assert extract_table(html) == expected

def test_extract_table_missing_rows():
    """Test extracting table with missing rows."""
    html = '''
    <table>
    </table>
    '''
    expected = []
    assert extract_table(html) == expected

def test_extract_table_malformed_html():
    """Test extracting table from malformed HTML."""
    html = '''
    <div>
        <table
            <tr><td>Data 1</td><td>Data 2</td>
    </div>
    '''
    # html5lib parser is very robust and can handle this
    expected = [['Data 1', 'Data 2']]
    assert extract_table(html) == expected

def test_extract_table_no_table():
    """Test extracting table when no table exists."""
    html = '<div><p>No table here</p></div>'
    expected = []
    assert extract_table(html) == expected
    
def test_extract_table_nested_elements():
    """Test extracting table with nested elements inside td."""
    html = '''
    <table>
        <tr>
            <td><span>Data</span> <b>1</b></td>
            <td><a href="#">Link</a></td>
        </tr>
    </table>
    '''
    expected = [['Data 1', 'Link']]
    assert extract_table(html) == expected

def test_extract_license_valid():
    """Test extracting a valid license."""
    text = "Company Name (Licença 12345-AMI)"
    assert extract_license(text) == "12345-AMI"

def test_extract_license_invalid():
    """Test extracting an invalid license or missing license."""
    text = "Company Name without license"
    assert extract_license(text) is None

def test_export_data(tmp_path):
    """Test data export to Excel."""
    # Data is list of lists
    data = [['Col1', 'Col2'], ['Val1', 'Val2']]
    filepath = os.path.join(tmp_path, "test_output.xlsx")
    
    export_data(data, filepath)
    
    assert os.path.exists(filepath)
    # The default pandas DataFrame constructor with list of lists makes the first row data, not columns, unless specified
    # So length will be 2
    df = pd.read_excel(filepath)
    assert len(df) == 2
