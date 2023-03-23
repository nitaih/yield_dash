from click import style
import pandas as pd
from dash import Dash, html, dcc
# import dash
# from dash import html
# import dash_html_components as html
# import dash_core_components as dcc
# from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update

data = pd.read_csv(r'C:\Users\nitaih\OneDrive - InnoValley Ltd\Dash_creations\yield_database.csv')
crop_list = data['crop'].unique()
year_list = data['year'].unique()
location_list = data['location'].unique()

# Create a dash application
app = Dash(__name__)

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True
app.layout = html.Div(children = [
    html.H1('Water Salinity Project - Yield dashboard', style={'textAlign':'left','color':'#503D36','font-size':30}),
    html.Div([
        # add next division for year selector
        html.Div([
            html.Div(
                [
                    html.H2('Select a Year', style={'margin-right': '2em', 'font-size': '15px'}),
                    ]
            ),
            dcc.Dropdown(id='input-year', 
            options=[{'label':i,'value':i} for i in year_list],
            value=2022,
            placeholder = 'Select a Year',
            style = {'width':'80%', 'padding':'3px', 'font-size': '15px', 'text-align-last' : 'center'}),
            ], style = {'display': 'flex'}),
            # add next division for crop selector
            html.Div([
                html.Div(
                    [
                        html.H2('Select a Crop', style={'margin-right': '2em', 'font-size': '15px'})
                        ]
                        ),
                        dcc.Dropdown(id= 'input-crop', 
                        options = [{'label':j, 'value':j} for j in crop_list],
                        placeholder='Select a Crop',
                        style={'width':'80%', 'padding':'3px', 'font-size': '15px', 'text-align-last' : 'center'}),
                        ], style = {'display': 'flex'}),
                        # add next division for location selector
                        html.Div([
                            html.Div(
                                [
                                    html.H2('Select Location', style={'margin-right': '2em', 'font-size': '15px'})
                                    ]
                                    ),
                                    dcc.Dropdown(id= 'input-location', 
                                    options = [{'label':k, 'value':k} for k in location_list],
                                    placeholder='Select Location',
                                    style={'width':'80%', 'padding':'3px', 'font-size': '15px', 'text-align-last' : 'center'}),
                                    ], style = {'display': 'flex'}),
                                    ]),
                                    # add graph divisions
                                    # html.Div([ ], id='plot1'),
                                    # html.Div([ ], id='plot2'),
                                    html.Div([
                                        html.Div([ ], id='plot1'),
                                        html.Div([ ], id='plot2')
                                        ], style={'display': 'flex'}),
                                    ])

@app.callback([
    Output(component_id='plot1', component_property='children'), 
    Output(component_id='plot2', component_property='children')],
    [
        Input(component_id='input-year', component_property='value'),
        Input(component_id='input-crop', component_property='value'),
        Input(component_id='input-location', component_property='value')],
        [
            State(component_id="plot1", component_property='children'), 
            State(component_id="plot2", component_property="children")])
# Add computation to callback function and return graph
def get_graph(year, crop, location, children1, children2):
    # filter year
    dfy = data[data['year'] == year]
    # filter crop
    dfc = dfy[dfy['crop'] == crop]
    # filter location
    dfl = dfc[dfc['location'] == location]
    if crop == 'onion':
        units = 'Large/Total Ratio'
    else: units = 'g'

    yield_fig = px.box(dfl,x='treatment',y='total yield (ton/dunam)', points='all', color='salinity', title='Total Yield per treatment')
    fruit_fig = px.box(dfl,x='treatment',y='fruit size', points='all', color='salinity', title='fruit size per treatment',labels={"fruit size": 'fruit size ({0})'.format(units)})
    return [dcc.Graph(figure=yield_fig), dcc.Graph(figure=fruit_fig)]
# Run the app
if __name__ == '__main__':
    app.run_server()