'''
This module contains the components factory functions that are used in the dash app.
'''
from dash import html
import dash_bootstrap_components as dbc
import database.queries as db
from utils import format_metric, format_season

def create_metrics_tabs(id='metric-tabs'):
    '''Create metric tabs element.'''
    metrics = ['points', 'wins', 'draws', 'losses', 'goals_for', 'goals_against', 'goal_difference']
    metric_options = [{'label': format_metric(metric), 'value': metric} for metric in metrics]

    metric_tabs = dbc.Col(dbc.Tabs(
            id=id,
            active_tab=metric_options[0]['value'],
            class_name='d-flex justify-content-center w-100 my-2',
            children = [
                dbc.Tab(label=option['label'], tab_id=option['value'])
                for option in metric_options
            ]
        ), md=8, xs=12)
    return metric_tabs

def create_season_select(id='season-select'):
    '''Create a season select element.'''
    season_ids = db.get_unique_season_ids()
    season_options = [{'label': format_season(season_id), 'value': season_id} for season_id in season_ids]
    season_select = dbc.Col(dbc.Select(
            id=id,
            options=season_options,
            placeholder=f'Select Season',
            className='w-100 my-2'
        ), md=4, xs=12)
    return season_select

def create_footer():
    footer = dbc.Row(
            dbc.Col(
                html.Footer(
                    children=[
                        html.P('Data Source: The English Women’s Football (EWF) Database, May 2024, ', 
                            className='text-center mb-0'),
                        html.A('https://github.com/probjects/ewf-database', 
                            href='https://github.com/probjects/ewf-database', 
                            className='text-center', target='_blank')
                    ],
                    className='py-2 border-top'
                ),
                width={'size': 12},
                className='d-flex justify-content-center align-items-center'
            ),
            className='mt-auto'
        )
    return footer

def generate_color_palette(num_colors):
    if num_colors <= 0:
        return []

    base_colors = ['#32DE8A', # Esmerald
                   '#2CA6A4', # Sea Green
                   '#64E9EE', # Light Blue  
                   '#449DD1', # Celestial Blue
                   '#3454D1', # Bright Blue
                   '#9448BC', # Purple
                   '#E980FC', # Violet
                   '#C154C1', # Fuchsia
                   '#FF007F', # Bright Pink
                   '#EB7BC0', # Pink
                   '#E0BAD7', # Light Pink
                ]
    
    base_rgb_colors = [tuple(int(c, 16) for c in (color[i:i+2] for i in (1, 3, 5))) for color in base_colors]

    color_palette = []
    for i in range(num_colors):
        pos = i / (num_colors - 1) * (len(base_colors) - 1)
        lower_idx = int(pos)
        upper_idx = min(lower_idx + 1, len(base_colors) - 1)
        weight = pos - lower_idx
        lower_color = base_rgb_colors[lower_idx]
        upper_color = base_rgb_colors[upper_idx]
        interpolated_color = [int(lower_color[j] * (1 - weight) + upper_color[j] * weight) for j in range(3)]
        color = f'rgb({interpolated_color[0]}, {interpolated_color[1]}, {interpolated_color[2]})'
        color_palette.append(color)

    return color_palette