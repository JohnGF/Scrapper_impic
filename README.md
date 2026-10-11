# IMPIC Web Scraper

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Web Scraping](https://img.shields.io/badge/Web%20Scraping-BeautifulSoup-green)

A modular, robust web scraping pipeline for extracting data from the IMPIC portal.

## Extraction Pipeline

```mermaid
graph LR
    A[Target Portal] --> B[Scraping Engine]
    B --> C[Parsed Dataset]
    C --> D[(Storage)]
```

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install requests beautifulsoup4 pandas html5lib openpyxl lxml
   ```

2. **Run Tests (Optional but recommended):**
   ```bash
   pip install pytest pytest-mock requests-mock
   pytest test_Scrapping.py
   ```

## Configuration Parameters

- `timeout`: Maximum wait time for API requests (default: 10s).
- `name`: Target page endpoint (e.g., `empresas-titulares-de-licenca-de-mediacao-imobiliaria`).
- Pagination ranges can be customized in the `main` block of `Scrapping.py`.

## Runnable Examples

To start the scraper and extract real estate license data into an Excel file:

```bash
python Scrapping.py
```

This will fetch the pages, extract the tabular data, and export it into an Excel file named `empresas-titulares-de-licenca-de-mediacao-imobiliaria.xlsx` in the current directory.
