

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

OptionList =[]
OptionList = spacex_df['Launch Site'].unique()


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                        'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                             id='site-dropdown',
                                             options=[
                                                      {'label': OptionList[0], 'value': OptionList[0]},
                                                      {'label': OptionList[1], 'value': OptionList[1]},
                                                      {'label': OptionList[2], 'value': OptionList[2]},
                                                      {'label': OptionList[3], 'value': OptionList[3]},
                                                      {'label': 'All sites', 'value': 'ALL'}
                                                      ],
                                             value='ALL',
                                             placeholder='Select a Launch Site here',
                                             searchable=True
                                             ),
                                
                                html.Br(),
                                
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[min_payload,max_payload]),
                                
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback (
               Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value')
               )

def get_pie(LaunchSite):
    if LaunchSite == 'ALL':
        ALL_df=spacex_df[['Launch Site', 'class']]
        ALL_df=ALL_df.groupby('class').count().reset_index()
        fig = px.pie(ALL_df, values='Launch Site', names='class',title='All Launch Sites')
    
    elif LaunchSite == 'CCAFS LC-40':
        is_CCAFS_LC_40 =  spacex_df['Launch Site']==LaunchSite
        CCAFS_LC_40_df = spacex_df[is_CCAFS_LC_40]
        CCAFS_LC_40_df = CCAFS_LC_40_df[['Launch Site', 'class']]
        CCAFS_LC_40_df = CCAFS_LC_40_df.groupby('class').count().reset_index()
        fig = px.pie(CCAFS_LC_40_df, values='Launch Site', names='class', title='Launch Site: CCAFS LC-40')
    
    elif LaunchSite == 'VAFB SLC-4E':
        is_VAFB_SLC_4E =  spacex_df['Launch Site']==LaunchSite
        VAFB_SLC_4E_df = spacex_df[is_VAFB_SLC_4E]
        VAFB_SLC_4E_df = VAFB_SLC_4E_df[['Launch Site', 'class']]
        VAFB_SLC_4E_df = VAFB_SLC_4E_df.groupby('class').count().reset_index()
        fig = px.pie(VAFB_SLC_4E_df, values='Launch Site', names='class', title='Launch Site: VAFB SLC-4E')
    
    elif LaunchSite == 'KSC LC-39A':
        is_ =  spacex_df['Launch Site']==LaunchSite
        _df = spacex_df[is_]
        _df = _df[['Launch Site', 'class']]
        _df = _df.groupby('class').count().reset_index()
        fig = px.pie(_df, values='Launch Site', names='class', title='Launch Site: KSC LC-39A')
    
    elif LaunchSite == 'CCAFS SLC-40':
        is_ =  spacex_df['Launch Site']==LaunchSite
        _df = spacex_df[is_]
        _df = _df[['Launch Site', 'class']]
        _df = _df.groupby('class').count().reset_index()
        fig = px.pie(_df, values='Launch Site', names='class', title='Launch Site: CCAFS SLC-40')
    
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback (
               Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id="payload-slider", component_property="value")]
               )

def get_scatter(LC,slider_range):

    low, high = slider_range

    if LC == 'ALL':
        is_range = spacex_df['Payload Mass (kg)'].between(low,high)
        df = spacex_df[['Launch Site','Payload Mass (kg)', 'class', 'Booster Version']]
        df = df[is_range]
        fig = px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version", title='All launch sites')
    
    if LC == 'CCAFS LC-40':

        is_site =  spacex_df['Launch Site'] == LC
        df = spacex_df[is_site]
        is_range = df['Payload Mass (kg)'].between(low,high)
        df = df[['Launch Site','Payload Mass (kg)', 'class', 'Booster Version']]
        df = df[is_range]
        fig = px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version", title='CCAFS LC-40')

    
    if LC == 'VAFB SLC-4E':
        is_site =  spacex_df['Launch Site'] == LC
        df = spacex_df[is_site]
        is_range = df['Payload Mass (kg)'].between(low,high)
        df = df[['Launch Site','Payload Mass (kg)', 'class', 'Booster Version']]
        df = df[is_range]
        fig = px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version", title='VAFB SLC-4E')
    
    if LC == 'KSC LC-39A':
        is_site =  spacex_df['Launch Site'] == LC
        df = spacex_df[is_site]
        is_range = df['Payload Mass (kg)'].between(low,high)
        df = df[['Launch Site','Payload Mass (kg)', 'class', 'Booster Version']]
        df = df[is_range]
        fig = px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version", title='KSC LC-39A')
    
    if LC == 'CCAFS SLC-40':
        is_site =  spacex_df['Launch Site'] == LC
        df = spacex_df[is_site]
        is_range = df['Payload Mass (kg)'].between(low,high)
        df = df[['Launch Site','Payload Mass (kg)', 'class', 'Booster Version']]
        df = df[is_range]
        fig = px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version", title='CCAFS SLC-40')
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
