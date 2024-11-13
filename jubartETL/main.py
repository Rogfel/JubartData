import os
import json
import zipfile
import argparse
import pandas as pd
from glob import glob
from datetime import datetime
from date_util import DateParser
from utils import get_mark
from api_claude import scraping_image


# Initialize parser
parser = argparse.ArgumentParser(prog='JubartData pipeline',
                                 description='Esta é a pipeline desenvolvida para gerar o datastet de JubartData supermarket')
date_parser = DateParser(default_year=datetime.now().year)

# Adding optional argument
parser.add_argument("--ocr", action='store_true', help="Carregar informação das imagens")
parser.add_argument("--format01", action='store_true', help="Formatar os nomes dos produtos em produto e marca")
parser.add_argument("--format02", action='store_true', help="Criar dois resgistros com os produtos duplicados em um só")
parser.add_argument("--format03", action='store_true', help="Formatar as datas")
parser.add_argument("--join", action='store_true', help="Unir novos dataset com os mais antigos")
parser.add_argument("--zip", action='store_true', help="Comprimir imagens em um zip e eliminar elas da pasta")

def string_to_json(string_data):
    try:
        # Parse the string into a Python object
        json_data = json.loads(string_data)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

if __name__ == '__main__':

    df_dataset = pd.DataFrame()
    args = parser.parse_args()
    if args.ocr:
    
        for sm_path in ['imagens_assai', 'imagens_atacadao', 'imagens_bigbox', 'imagens_carrefour',
                        'imagens_oba', 'imagens_paodeacucar', 'imagens_veneza']:
            print('####', sm_path)
            for image in glob(sm_path + '/*.webp'):
                print(image)
                data = scraping_image(image, image_type='image/jpeg')

                data_json = string_to_json(data[0].replace('\n', ''))

                sm = sm_path.split('_')[-1]
                df_temp = pd.DataFrame(data_json)
                df_temp['date_source'] = datetime.now().strftime("%Y-%m-%d")
                df_temp['supermarket'] = sm
                df_temp['tablode_source'] = image

                df_dataset = pd.concat([df_dataset, df_temp], axis=0, ignore_index=True)
                
        df_dataset.to_csv('dataset/sm_' + datetime.now().strftime("%Y_%m_%d") +'_v1.csv', index=False)
    
    if args.format02:

        new_df = pd.read_csv('dataset/sm_' + datetime.now().strftime("%Y_%m_%d") +'_v2.csv').drop_duplicates()
        # new_df = pd.read_csv('dataset/sm_total2.csv').drop_duplicates()
        with open('list_marks.json', 'r', encoding='utf-8') as file:
            data = json.loads(file.read())
        
        new_df['marca'] = new_df['nome'].apply(lambda x: get_mark(x.lower(), data['marks']))
        new_df['produto'] = new_df.apply(lambda x: x['nome'].lower().replace(x['marca'],
                                                                     '').strip().replace('  ', ' ') if x['marca'] else x['nome'],
                                         axis=1)
        new_df.to_csv('dataset/sm_' + datetime.now().strftime("%Y_%m_%d") +'_v3.csv', index=False)
        # new_df.to_csv('dataset/sm_total3.csv', index=False)
    
    if args.format01:

        novos_registros = []
        new_df = pd.read_csv('dataset/sm_' + datetime.now().strftime("%Y_%m_%d") +'_v1.csv').drop_duplicates()
        # new_df = pd.read_csv('dataset/sm_total.csv')
    
        # Iterar sobre cada registro do DataFrame
        for idx, row in new_df.iterrows():
            if ' ou ' in str(row['nome']):
                # Dividir o nome em duas partes
                nomes = row['nome'].split(' ou ')
                
                # Criar dois novos registros, um para cada nome
                for nome in nomes:
                    novo_registro = row.copy()
                    novo_registro['nome'] = nome.strip()
                    novos_registros.append(novo_registro)
            else:
                # Manter registro original se não contiver "ou"
                novos_registros.append(row)
        
        # Criar novo DataFrame com os registros expandidos
        df_expandido = pd.DataFrame(novos_registros)
        df_expandido = df_expandido.reset_index(drop=True)

        df_expandido.to_csv('dataset/sm_' + datetime.now().strftime("%Y_%m_%d") +'_v2.csv', index=False)
        # df_expandido.to_csv('dataset/sm_total2.csv', index=False)

    if args.format03:

        new_df = pd.read_csv('dataset/sm_' + datetime.now().strftime("%Y_%m_%d") +'_v3.csv').drop_duplicates()
        # new_df = pd.read_csv('dataset/sm_total3.csv')

        for col in ['data_ini', 'data_fim', 'date_source']:
            new_df[col + '_format'] = new_df[col].apply(lambda x: date_parser.parse(x))

        new_df.to_csv('dataset/sm_' + datetime.now().strftime("%Y_%m_%d") +'_v4.csv', index=False)
        # new_df.to_csv('dataset/sm_total4.csv', index=False)
    
    if args.join:

        new_df = pd.read_csv('dataset/sm_' + datetime.now().strftime("%Y_%m_%d") +'_v2.csv')
        total_df = pd.read_csv('dataset/sm_total.csv')

        df_dataset = pd.concat([total_df, new_df], axis=0, ignore_index=True)
        df_dataset.to_csv('dataset/sm_total.csv', index=False)

    if args.zip:

        for sm_path in ['imagens_assai', 'imagens_atacadao', 'imagens_bigbox', 'imagens_carrefour',
                        'imagens_oba', 'imagens_paodeacucar', 'imagens_veneza']:
            print('####', sm_path)
            webp_files = glob(sm_path + '/*.webp')

            if not webp_files:
                print('Nenhum arquivo .webp encontrado na pasta')
                continue

            zip_filename = os.path.join(sm_path, 'webp_' + datetime.now().strftime("%Y_%m_%d") + '.zip')

            # Compacta todos os arquivos em um único zip
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in webp_files:
                    zipf.write(file, os.path.basename(file))
            print(f'Compactado criado: {zip_filename}')

            for file in webp_files:
                os.remove(file)
            print('Removido todas as imagens')