import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from scrapping import selemium
from urllib.parse import urlparse


def save_pages(page, name, path='downloaded_pages'):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f'{path}/page_{name}.html', "w", encoding="utf-8") as f:
            f.write(page)

def download_image(url, path='imagens_carrefour'):
    # Crear el directorio de destino si no existe
    if not os.path.exists(path):
        os.makedirs(path)
    
    # Obtener el nombre del archivo de la URL
    nombre_archivo = os.path.basename(urlparse(url).path)
    if not nombre_archivo:
        nombre_archivo = 'imagen_sin_nombre.jpg'
    
    # Ruta completa para guardar la imagen
    ruta_completa = os.path.join(path, nombre_archivo)
    
    # Realizar la solicitud GET para descargar la imagen
    response = requests.get(url, stream=True)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Guardar la imagen
        with open(ruta_completa, 'wb') as archivo:
            for chunk in response.iter_content(1024):
                archivo.write(chunk)
        print(f"Imagen descargada con éxito: {ruta_completa}")
        return True
    else:
        print(f"Error al descargar la imagen. Código de estado: {response.status_code}")
        return False
    

def download_mult_imagens(urls, path='imagens_carrefour'):
    result = []
    for url in urls:
        download_image(url, path=path)
        result.append(url.split('/')[-1])
    return result

def download_market_page(url='link', class_img='tc', path='imagens_carrefour'):

    try:
        # download html
        page = selemium.descargar_pagina_selenium(url=url)

        # extract imagens
        soup = BeautifulSoup(page, 'html.parser')
        if tabloide_link:=soup.find_all('div', class_=class_img):
             tabloide_link = [link.find('img').get('src') for link in tabloide_link if link.find('img')]
             return download_mult_imagens(tabloide_link, path=path)
        
    except requests.exceptions.RequestException as e:
        print(f"Tentativa falhou: {e}")