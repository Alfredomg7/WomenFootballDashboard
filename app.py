import components as comp
from dash import Dash, html, dcc, Input, Output
from dash_bootstrap_templates import load_figure_template
from database.setup import setup, check_database_exists
import database.queries as db
import dash_bootstrap_components as dbc
import plotly.express as px
from utils import format_season, format_metric

# Initialize the app
def create_app():
    load_figure_template('quartz')
    app = Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ], suppress_callback_exceptions=True)

    # Create components
    season_select = comp.create_season_select()
    metric_tabs = comp.create_metrics_tabs()
    team_stats_bar_chart = dcc.Graph(id='team-stats-chart', className='my-3')
    team_stats_scatter_chart = dcc.Graph(id='team-stats-scatter-chart', className='my-3')
    footer = comp.create_footer()


    # Combine all components into the layout
    app.layout = html.Div([
    html.H1('England Women\'s Football League Stats (2011-2023)', className='text-center mt-3'),
    dbc.Row([season_select, metric_tabs], className='d-flex justify-content-center'),
    team_stats_bar_chart,
    team_stats_scatter_chart,
    footer
    ], className='d-flex flex-column h-100')

    # Callback to update the bar chart
    @app.callback(
    Output('team-stats-chart', 'figure'),
    [Input('season-select', 'value'),
        Input('metric-tabs', 'active_tab')]
    )
    def update_team_stats_bar_chart(season_id, metric):
        if not season_id:
            return px.bar(title='Select a season to view team stats.')

        df = db.get_team_performance_metrics_by_season(season_id, metric)

        if df.empty:
            return px.bar(title='No data found for the selected metric and season')

        labels = {'total': format_metric(metric), 'team_name': 'Team'} 

        fig = px.bar(df, x='team_name', y='total', 
                        title=f"Total {format_metric(metric)} by Team in {format_season(season_id)}", 
                        labels=labels,
                        color='team_name',
                        color_discrete_sequence=comp.generate_color_palette(12)
                    )

        fig.update_xaxes(title_text='', tickangle=-45)
        fig.update_yaxes(title_text=format_metric(metric), range=[0, df['total'].max() + 5])
        fig.update_layout(
            title_font_size=24,
            title_x=0.5,
            xaxis_title_font_size = 16,
            yaxis_title_font_size = 16,
            showlegend=False
        )
        return fig

    # Callback to update the scatter chart
    @app.callback(
    Output('team-stats-scatter-chart', 'figure'),
    [Input('season-select', 'value'),
        Input('metric-tabs', 'active_tab')]
    )
    def update_team_stats_scatter_chart(season_id, metric):
        metric_column_mapping = {
        'points': 'points',
        'wins': 'win',
        'draws': 'draw',
        'losses': 'loss',
        'goals_for': 'goals_for',
        'goals_against': 'goals_against',
        'goal_difference': 'goal_difference'
        }
        if not season_id:
            return px.scatter(title='Select a season to view team stats.')

        eq_metric = metric_column_mapping[metric]
        df = db.get_team_performance_metrics_by_match(season_id, eq_metric)

        if df.empty:
            return px.scatter(title='No data found for the selected season and metric.')

        labels = {'total': format_metric(metric), 'date': 'Date', 'team_name': 'Team', 'opponent_name': 'Opponent'}

        fig = px.scatter(data_frame=df, x='date', y='total', color='team_name', 
                            title=f'{format_metric(metric)} Over Matches for {format_season(season_id)}',
                            labels=labels,
                            color_discrete_sequence=comp.generate_color_palette(12),
                            hover_data = {'date': True, 'team_name': True, 'opponent_name': True, 'total': True}
                        )

        fig.update_yaxes(title_text=format_metric(metric), range=[0, df['total'].max() + 5])
        fig.update_xaxes(title_text='', tickangle=-45)
        fig.update_layout(
            title_font_size=24,
            title_x=0.5,
            xaxis_title_font_size=16,
            yaxis_title_font_size=16,
        )
        fig.update_traces(marker_size=15)
        return fig

    return app

if __name__ == '__main__':
    # create database if it does not exist
    if not check_database_exists():
        setup()

    # Create the app from the factory function
    app = create_app()
    
    # Run the app
    app.run_server(debug=False)
