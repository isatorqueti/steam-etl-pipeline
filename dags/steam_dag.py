from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import sys
import os

sys.path.insert(0, '/opt/airflow/src')

from extract_data import extract_ranking, extract_apps
from load_data import load_steam_data
from transform_data import data_transformations
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

API_KEY = os.getenv('API_KEY')

url_ranking = f'https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1/?key={API_KEY}'
url_apps = f'https://api.steampowered.com/IStoreService/GetAppList/v1/?key={API_KEY}&include_games=true'

@dag(
    dag_id='steam_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    },
    description='Steam Pipeline',
    schedule='0 */1 * * * ',
    start_date=datetime(2026, 2, 7),
    catchup=False,
)

def steam_pipeline():

    @task
    def extract():
        extract_ranking(url_ranking, "steam_ranking.json")
        extract_apps(url_apps, "steam_apps.json")

    @task
    def transform():
        df = data_transformations()
        df.to_parquet('/opt/airflow/data/temp_data.parquet', index=False)

    @task
    def load():
        import pandas as pd
        df = pd.read_parquet('/opt/airflow/data/temp_data.parquet')
        load_steam_data('steam_data', df)

    extract() >> transform() >> load()

steam_pipeline()