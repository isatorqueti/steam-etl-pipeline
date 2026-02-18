# from src.extract_data import extract_ranking, extract_apps
# from src.load_data import load_steam_data
# from src.transform_data import data_transformations

# import os
# from pathlib import Path
# from dotenv import load_dotenv

# import logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
# load_dotenv(env_path)

# API_KEY = os.getenv('api_key')

# url_ranking = f'https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1/?key={API_KEY}'
# url_apps = f'https://api.steampowered.com/IStoreService/GetAppList/v1/?key={API_KEY}&include_games=true'

# table_name = 'steam_data'

# def pipeline():
#     try:
#         logging.info("ETAPA 1: EXTRACT RANKING")
#         extract_ranking(url_ranking, "steam_ranking.json")

#         logging.info("ETAPA 2: EXTRACT APPS")
#         extract_apps(url_apps, "steam_apps.json")

#         logging.info("ETAPA 2: TRANSFORM")
#         df = data_transformations()
        
#         logging.info("ETAPA 3: LOAD")
#         load_steam_data(table_name, df)

#         print("\n" + "="*60)
#         print("✅ Pipeline concluído com sucesso!")
#         print("="*60)

#     except Exception as e:
#         logging.error(f"❌ ERRO no Pipeline: {e}")
#         import traceback
#         traceback.print_exc()

# pipeline()