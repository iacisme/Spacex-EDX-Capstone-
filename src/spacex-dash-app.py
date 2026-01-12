# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash import Input, Output, callback
import plotly.express as px

# Dataset location
path_to_file = '../data/00_Datasets/00_Raw/CSVs/'
file_name = 'spacex_launch_dash.csv'

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(
    path_to_file + file_name,
    index_col = 'Unnamed: 0'
)

# Replace 'CCAFS LC-40' to 'CCAFS SLC-40', it's the same site
spacex_df['Launch Site'] = spacex_df['Launch Site'].replace(
    'CCAFS LC-40',
    'CCAFS SLC-40'
)
# Create a list of Launch Sites to use in the drop drop-down for Task #1
launch_site_lst = sorted(spacex_df['Launch Site'].unique().tolist())
# Add a value to the list
launch_site_lst.insert(0, 'All Sites')
# Create a list of labels to be used in the dropdown required for Task #1
launch_site_options_lst = [{'label': site, 'value': site} for site in launch_site_lst]

# Markers that will be used in the range slider
marks_dct = {
    0 : '0 KG',
    1000 : '1000 KG',
    2000 : '2000 KG',
    3000 : '3000 KG',
    4000 : '4000 KG',
    5000 : '5000 KG',
    6000 : '6000 KG',
    7000 : '7000 KG',
    8000 : '8000 KG',
    9000 : '9000 KG',
    9600: '9600 KG'
}

# Calculate min / max payload mass
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children = [
        html.H1(
            'SpaceX Launch Records Dashboard',
            style = {
                'textAlign': 'center', 
                'color': '#503D36',
                'font-size': 40
            }
        ),
        
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        # dcc.Dropdown(id='site-dropdown',...)
        dcc.Dropdown(
            id = 'site-dropdown',
            options = launch_site_options_lst,
            value = 'All Sites',
            placeholder = 'Select a Launch Site'
        ),

        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(
            dcc.Graph(
                id = 'success-pie-chart'
            )
        ),
        html.Br(),

        html.P("Payload range (Kg):"),
        
        # TASK 3: Add a slider to select payload range
        #dcc.RangeSlider(id='payload-slider',...)
                dcc.RangeSlider(
            id = 'payload-slider',
            min = min_payload,
            max = max_payload,
            step = 1000,
            marks = marks_dct,
            value = [
                min_payload,
                max_payload
            ]
        ),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(
            dcc.Graph(
                id = 'success-payload-scatter-chart'
            )
        ),
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@callback(
    Output(component_id = 'success-pie-chart', component_property = 'figure'),
    Input(component_id = 'site-dropdown', component_property = 'value')
)
def pie_chart(launch_site):
    # Create a dataset based on user input
    if launch_site == 'All Sites':
        # Total successful launch count for all sites
        df = spacex_df[spacex_df['class'] == 1]
        graph_title = 'Total successful launches by site'
        names_var = 'Launch Site'
        class_var = 'class'
    else:
        # Success vs Failed counts for selected launch site
        df = spacex_df[spacex_df['Launch Site'] == launch_site]
        graph_title = f'Total successful Launches for site <b>{launch_site}</b>'
        names_var = 'class'
        class_var = None

    fig = px.pie(
        df,
        names = names_var,
        values = class_var,
        title = graph_title,
        color = names_var,
        color_discrete_map = {
            0 : 'red',
            1 : 'blue'
        }
    )

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@callback(
    Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
    Input(component_id = 'site-dropdown', component_property = 'value'),
    Input(component_id = 'payload-slider', component_property = 'value')
)
def scatter_plot(launch_site, payload_mass_lst):

    # Create a dataset based on user input
    if launch_site == 'All Sites':
        # Filter the dataset for the selected range of payload mass
        df = spacex_df[
            (spacex_df['Payload Mass (kg)'] >= payload_mass_lst[0]) &
            (spacex_df['Payload Mass (kg)'] <= payload_mass_lst[1])
        ]
        graph_title = 'Correlation between Payload and Success for all Sites'
    else:
        # Create a dataset based on the user selected launch site
        df = spacex_df[spacex_df['Launch Site'] == launch_site]
        # Filter the dataset for the selected range of payload mass
        df = df[
            (df['Payload Mass (kg)'] >= payload_mass_lst[0]) &
            (df['Payload Mass (kg)'] <= payload_mass_lst[1])
        ]
        graph_title = f'Payload and Booster Versions for site <b>{launch_site}</b>'

    fig = px.scatter(
        df,
        x = 'Payload Mass (kg)',
        y = 'class',
        color = 'Booster Version Category',
        title = graph_title
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run()
