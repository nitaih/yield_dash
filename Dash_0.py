from click import style
import pandas as pd
import geopandas as gpd
from shapely import wkt
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
                                        html.Div([
                                            html.Div([ ], id='plot1'),
                                            html.Div([ ], id='plot2'),]),
                                        html.Div([
                                            html.H2('Yield Map', style={'margin-right': '2em', 'font-size': '15px'}),
                                            html.Div([ ], id='plot3')
                                            ], style={'width':'80%'})  
                                        ], style = {'display': 'flex'}),
                                    
                                        
        ])

@app.callback([
    Output(component_id='plot1', component_property='children'), 
    Output(component_id='plot2', component_property='children'),
    Output(component_id='plot3', component_property='children')],
    [
        Input(component_id='input-year', component_property='value'),
        Input(component_id='input-crop', component_property='value'),
        Input(component_id='input-location', component_property='value')],
        [
            State(component_id="plot1", component_property='children'), 
            State(component_id="plot2", component_property="children"),
            State(component_id="plot3", component_property="children")])
# Add computation to callback function and return graph
def get_graph(year, crop, location, children1, children2, children3):
    # filter year
    dfy = data[data['year'] == year]
    # filter crop
    dfc = dfy[dfy['crop'] == crop]
    # filter location
    dfl = dfc[dfc['location'] == location]
    if crop == 'onion':
        units = 'Large/Total Ratio'
    else: units = 'g'

    if crop == 'dates':
        if location == 'merav':
            coord = [32.45229, 35.52110]
            zoom = 17
        elif location == 'havat eden':
            coord = [32.46669, 35.49053]
            zoom = 17
    elif crop == 'mango':
        if location == 'merav':
            coord = [32.45752, 35.45842] 
            zoom = 18
        elif location == 'nir david':
            coord = [32.50266, 35.44758]
            zoom = 17.5
    elif crop == 'onion':
        coord = [32.46820, 35.48803]
        zoom = 17.5

    dfl['geometry'] = dfl['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(dfl, crs='epsg:4326')
    

    yield_fig = px.box(dfl,x='treatment',y='total yield (ton/dunam)', points='all', color='salinity', title='Total Yield per treatment')
    fruit_fig = px.box(dfl,x='treatment',y='fruit size', points='all', color='salinity', title='fruit size per treatment',labels={"fruit size": 'fruit size ({0})'.format(units)})
    map_fig = px.choropleth_mapbox(gdf,
                           geojson=gdf.geometry,
                           locations=gdf.index,
                           color_continuous_scale = 'greens',
                           hover_name="treatment",
                           hover_data=["salinity", "water amount"],
                           color="total yield (ton/dunam)",
                           center={"lat": coord[0], "lon": coord[1]}, #35.44758,32.50266
                        #    mapbox_style="open-street-map",
                           zoom=zoom,
                           title='Yield Map')

    map_fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "Google Hybrid",
                "source": [
                    "http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}"
                ]
            }
        ])
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return [dcc.Graph(figure=yield_fig), dcc.Graph(figure=fruit_fig), dcc.Graph(figure=map_fig)]
# Run the app
if __name__ == '__main__':
    app.run_server()