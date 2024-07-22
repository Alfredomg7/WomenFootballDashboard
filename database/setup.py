import csv
import os
import sqlite3

def create_tables(conn):
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                match_id TEXT PRIMARY KEY,
                season_id TEXT,
                season TEXT,
                tier INTEGER,
                division TEXT,
                match_name TEXT,
                date TEXT,
                attendance INTEGER,
                home_team_id TEXT,
                home_team_name TEXT,
                away_team_id TEXT,
                away_team_name TEXT,
                score TEXT,
                home_team_score INTEGER,
                away_team_score INTEGER,
                home_team_score_margin INTEGER,
                away_team_score_margin INTEGER,
                home_team_win INTEGER,
                away_team_win INTEGER,
                draw INTEGER,
                result TEXT,
                note TEXT,
                FOREIGN KEY (match_id) REFERENCES appearances (match_id)
            )'''),
        conn.execute('''
            CREATE TABLE IF NOT EXISTS appearances (
                season_id TEXT,
                season TEXT,
                tier INTEGER,
                division TEXT,
                match_id TEXT,
                match_name TEXT,
                date TEXT,
                attendance INTEGER,
                team_id TEXT,
                team_name TEXT,
                opponent_id TEXT,
                opponent_name TEXT,
                home_team TEXT,
                away_team TEXT,
                goals_for INTEGER,
                goals_against INTEGER,
                goal_difference INTEGER,
                result TEXT,
                win INTEGER,
                loss INTEGER,
                draw INTEGER,
                note TEXT,
                points INTEGER
            )''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS standings (
                season_id TEXT,
                season TEXT,
                tier INTEGER,
                division TEXT,
                position TEXT,
                team_id TEXT,
                team_name TEXT,
                played INTEGER,
                wins INTEGER,
                draws INTEGER,
                losses INTEGER,
                goals_for INTEGER,
                goals_against INTEGER,
                goal_difference INTEGER,
                points INTEGER,
                point_adjustment INTEGER,
                season_outcome TEXT
            )''')
    except sqlite3.OperationalError as e:
        print(f'Operational error during table creation: {e}')
    except sqlite3.DatabaseError as e:
        print(f'Database error during table creation: {e}')
    except Exception as e:
        print(f'An unexpected error occurred during table creation: {e}')

def execute_bulk_insert(conn, query, data):
    try:
        with conn:
            conn.executemany(query, data)
    except Exception as e:
        print(f'An error occurred during bulk insert: {e}')

def populate_table_from_csv(conn, query, csv_file):
    try:
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            # Convert CSV rows to tuples
            data_to_insert = [tuple(row.values()) for row in csv_reader]
            execute_bulk_insert(conn, query, data_to_insert)
    except Exception as e:
        print(f'An error occurred during table population: {e}')

def populate_tables(conn):
    ewf_matches = 'data/ewf_matches.csv'
    ewf_appearances = 'data/ewf_appearances.csv'
    ewf_standings = 'data/ewf_standings.csv'

    populate_table_from_csv(
        conn,
        '''INSERT INTO matches (
            season_id, season, tier, division, match_id, match_name, date, attendance,
            home_team_id, home_team_name, away_team_id, away_team_name, score,
            home_team_score, away_team_score, home_team_score_margin, away_team_score_margin,
            home_team_win, away_team_win, draw, result, note
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        ewf_matches
    )

    populate_table_from_csv(
        conn,
        '''INSERT INTO appearances (
            season_id, season, tier, division, match_id, match_name, date, attendance,
            team_id, team_name, opponent_id, opponent_name, home_team, away_team,
            goals_for, goals_against, goal_difference, result, win, loss, draw, note, points
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        ewf_appearances
    )
    populate_table_from_csv(
        conn,
        '''INSERT INTO standings (
            season_id, season, tier, division, position, team_id, team_name, played, wins, draws, losses, goals_for, goals_against, goal_difference, points, point_adjustment, season_outcome
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        ewf_standings
    )

def setup():
    database_path = 'database/ewf.db'
    os.makedirs(os.path.dirname(database_path), exist_ok=True)

    print('Setting up database...')
    try:
        with sqlite3.connect(database_path) as conn:
            create_tables(conn)
            populate_tables(conn)
            conn.commit()
            print('Database setup complete!')
    except sqlite3.OperationalError as e:
        print(f'Operational error during setup: {e}')
    except sqlite3.DatabaseError as e:
        print(f'Database error during setup: {e}')
    except Exception as e:
        print(f'An unexpected error occurred during setup: {e}')

if  __name__ == '__main__':
    setup()
