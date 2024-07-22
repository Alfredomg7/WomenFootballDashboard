'''
This module contains utility functions that are used in the dash app.
'''
def format_season(season_id):
    '''Format the season_id into a readable format.'''
    parts = season_id.split('-')
    start_year = parts[1]
    end_year = parts[2]

    if len(parts) == 5:
        label = f'{start_year}-{end_year} Season {parts[3]}'
    else:
        label = f'{start_year}-{end_year} Season'
    return label

def format_metric(metric):
    '''Format the metric into a readable format.'''
    formatted = metric.replace('_', ' ').title()
    return formatted