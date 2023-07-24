from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import pandas as pd
from tqdm import tqdm
import re
import csv

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
start_url = 'http://free-proxy.cz/'
driver.get(start_url)

op = driver.find_element(By.XPATH, '//*[@id="frmsearchFilter-protocol-1"]')
op.click()
filter_proxy = driver.find_element(By.XPATH, '//*[@id="frmsearchFilter-send"]')
filter_proxy.click()
export = driver.find_element(By.ID, 'clickexport')
export.click()

# Extracción del html de la página
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
div_content = soup.find('div', {'id':'zkzk'}).get_text()

#Limpieza
clean = re.sub(r'\.$', '', div_content).strip()

#Utilizar split para extraer las direcciones IP y los puertos
proxies_list = [proxy.strip() for proxy in div_content.split('<br>') if proxy.strip()]
# Convertir la lista en un diccionario
proxies_list = [{'http':f'http://{proxy}'} for proxy in proxies_list]

# Tabla para guardar las direcciones IP y los puertos
archivo_csv = 'proxies.csv'
with open(archivo_csv, 'w', newline='') as file:
    fieldname = ['http']
    writer = csv.DictWriter(file, fieldnames=fieldname)
    if file.tell() ==0:
        writer.writeheader()
    for proxy in proxies_list:
        writer.writerow(proxy)

#print(div_content)