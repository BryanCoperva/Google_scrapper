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

# Se crean las opciones para conectarse a la página de los proxys
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
start_url = 'http://free-proxy.cz/'
driver.get(start_url)



#op = driver.find_element(By.XPATH, '//*[@id="frmsearchFilter-protocol-1"]')
#op.click()
#filter_proxy = driver.find_element(By.XPATH, '//*[@id="frmsearchFilter-send"]')
#filter_proxy.click()
export = driver.find_element(By.ID, 'clickexport')
export.click()

# Extracción del html de la página
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
div_content = soup.find('div', {'id':'zkzk'}).decode_contents()

#Utilizar split para extraer las direcciones IP y los puertos
#proxies_list = [proxy.strip() for proxy in div_content.split('<br>') if proxy.strip()]

# Utilizar expresión regular para extraer las direcciones IP y los puertos
proxies_list = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', div_content)

# Tabla para guardar las direcciones IP y los puertos
archivo_csv = 'proxies.csv'
with open(archivo_csv, 'w', newline='') as file:
    fieldnames = ['http']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for proxy in proxies_list:
        writer.writerow({'http': f'http://{proxy}'})

#print(div_content)