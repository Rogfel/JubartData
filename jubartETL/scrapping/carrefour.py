import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from scrapping import selemium, utils


LINK = 'https://www.carrefour.com.br/folheto-digital/festival-do-pescado/BWL/152064'




def download_market_page(name, url=LINK):

    try:
        # download html
        page = selemium.descargar_pagina_selenium(url=url)
        # save html
        formatted_datetime = datetime.now().strftime("%Y_%m_%d")
        # utils.save_pages(page=page, name='carrefour_' +name + '_' + formatted_datetime)

        # extract imagens
        soup = BeautifulSoup(page, 'html.parser')
        if tabloide_link:=soup.find_all('div', class_='tc'):
             tabloide_link = [link.find('img').get('src') for link in tabloide_link if link.find('img')]
             return utils.download_mult_imagens(tabloide_link)
             
        
    except requests.exceptions.RequestException as e:
            print(f"Tentativa Carrefour falhou: {e}")


def download_principal_page(url=LINK):

    try:
        # download html
        page = selemium.descargar_pagina_selenium(url=url)
        # save html
        formatted_datetime = datetime.now().strftime("%Y_%m_%d")
        utils.save_pages(page=page, name='carrefour_principal_' + formatted_datetime)

        # extract markets info
        soup = BeautifulSoup(page, 'html.parser')
        if markets:=soup.find_all('div', class_='dcarrefourbr-carrefour-components-0-x-card carrefourbr-carrefour-components-0-x-flyerb'):
             markets = [{
                        'name': market.find('h3').get_text(),
                        'data': [p.get_text() for p in market.find_all('p')],
                        'link': market.find('a').get('href')
                         } for market in markets]
             return markets
        return None             
        
    except requests.exceptions.RequestException as e:
            print(f"Tentativa Carrefour falhou: {e}")

            