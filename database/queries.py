import logging
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///database/ewf.db')
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def get_team_performance_metrics_by_match(season_id, metric):
    try:
        query = f'''
                SELECT
                    date,
                    team_name,
                    opponent_name,
                    SUM({metric}) AS total
                FROM
                    appearances
                WHERE
                    season_id = ?
                GROUP BY
                    date,
                    team_name
                ORDER BY
                    date,
                    team_name
                '''
        df = pd.read_sql(query, engine, params=(season_id,))
        if df.empty:
            logging.error("No data found for the specified season.")
        return df
    except Exception as e:
        logging.error(f'An error occurred during get_team_performance_metrics query: {e}')
        return pd.DataFrame()

def get_team_performance_metrics_by_season(season_id, metric):
    try:
        query = f'''
                SELECT 
                    team_name, 
                    SUM({metric}) AS total
                FROM
                    standings
                WHERE  
                    season_id = ?
                GROUP BY
                    team_name
                ORDER BY
                    total DESC
                '''
        df = pd.read_sql(query, engine, params=(season_id,))
        if df.empty:
            logging.error("No data found for the specified season.")
        return df
    except Exception as e:
        logging.error(f'An error occurred during get_team_performance_metrics query: {e}')
        return pd.DataFrame()

def get_unique_season_ids():
    try:
        query = '''
                SELECT DISTINCT season_id
                FROM standings
                '''
        df = pd.read_sql(query, engine)
        if df.empty:
            logging.error("No data found for season_id.")
        return df['season_id'].tolist()
    except Exception as e:
        logging.error(f'An error occurred during get_unique_season_ids query: {e}')
        return []
    
def get_unique_team_names():
    try:
        query = '''
                SELECT DISTINCT team_name
                FROM standings
                ORDER BY team_id DESC
                '''
        df = pd.read_sql(query, engine)
        if df.empty:
            logging.error("No data found for team_name.")
        return df['team_name'].tolist()
    except Exception as e:
        logging.error(f'An error occurred during get_unique_team_names query: {e}')
        return []