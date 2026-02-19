import requests
import json
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_ranking(url:str, filename:str) -> list:
    
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        logging.error("Erro na requisição")
        return []
    
    if not data:
        logging.warn("Nenhum dado retornado")
        return []
    
    output_path = f'data/{filename}'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

    logging.info(f"Arquivo salvo em {output_path}")
    return data

def extract_apps(url_apps:str, filename:str) -> list:
    all_apps = []
    last_appid = None
    more_results = True

    while more_results:
        if last_appid:
            current_url = f'{url_apps}&last_appid={last_appid}'
        else:
            current_url = url_apps

        response = requests.get(current_url)

        if response.status_code != 200:
            logging.error("Erro na requisição")
            return []

        data_apps = response.json()

        if 'apps' in data_apps['response']:
            batch = data_apps['response']['apps']
            all_apps.extend(batch)
            logging.info(f"Baixando... Total carregado: {len(all_apps)}")

        more_results = data_apps['response'].get('have_more_results', False)
        last_appid = data_apps['response'].get('last_appid')
    
    output_path = f'data/{filename}'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    final_data_apps = {'applist': {'apps': all_apps}}

    with open(output_path, 'w') as f:
        json.dump(final_data_apps, f, indent=4)

    logging.info(f"Arquivo salvo em {output_path}")
    return final_data_apps