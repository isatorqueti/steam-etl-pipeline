import pandas as pd
from pathlib import Path
import json
from datetime import datetime

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_ranking = Path(__file__).parent.parent / 'data' / 'steam_ranking.json'
path_apps = Path(__file__).parent.parent / 'data' / 'steam_apps.json'

columns_names_to_drop = ['last_modified', 'price_change_number']
columns_names_to_rename = {
    "appid": "appid",
    "name": "game_title",
    "concurrent_in_game": "player_count"
}

def create_ranking_dataframe(path_ranking:str) -> pd.DataFrame:
    logging.info("\n→ Criando Ranking DataFrame")

    if not path_ranking.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path_ranking}")

    with open(path_ranking) as f:
        data_ranking = json.load(f)

    df_ranking = pd.json_normalize(data_ranking['response']['ranks'])
    logging.info(f"✓ Ranking DataFrame criado com {len(df_ranking)} linhas")
    return df_ranking

def create_apps_dataframe(path_apps:str) -> pd.DataFrame:
    logging.info("\n→ Criando Apps DataFrame")

    if not path_apps.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path_apps}")

    with open(path_apps) as f:
        data_apps = json.load(f)

    df_apps = pd.json_normalize(data_apps['applist']['apps'])
    logging.info(f"✓ Apps DataFrame criado com {len(df_apps)} linhas")
    return df_apps

def df_merge(df_ranking: pd.DataFrame, df_apps: pd.DataFrame) -> pd.DataFrame:
    logging.info(f"\n→ Mergeando os DataFrames Ranking e Apps")
    df_final = df_ranking.merge(df_apps, on="appid", how="left")
    logging.info("✓ Mergeados com sucesso")
    return df_final

def drop_columns(df: pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:
    logging.info(f"\n→ Removendo colunas: {columns_names}")
    df = df.drop(columns=columns_names)
    logging.info(f"✓ Colunas removidas - {len(df.columns)} colunas restantes")
    return df 

def rename_columns(df: pd.DataFrame, columns_names:dict[str, str]) -> pd.DataFrame:
    logging.info(f"\n→ Renomeando {len(columns_names)} colunas...")
    df = df.rename(columns=columns_names)
    logging.info("✓ Colunas renomeadas")
    return df

def null_normalize(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("\n→ Tratando dados nulos")
    df['game_title'] = df['game_title'].fillna("Desconhecido")
    logging.info("✓ Dados nulos tratados")
    return df

def data_transformations():
    print("\n Iniciando transformações")
    df_ranking = create_ranking_dataframe(path_ranking)
    df_apps = create_apps_dataframe(path_apps)
    df = df_merge(df_ranking, df_apps)
    df = drop_columns(df, columns_names_to_drop)
    df = rename_columns(df, columns_names_to_rename)
    df = null_normalize(df)
    df['extracted_at'] = datetime.now()
    logging.info("✓ Transformações concluídas\n")
    return df