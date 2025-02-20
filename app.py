from dash import Dash, html, dash_table, dcc, callback, Output, Input, State, no_update
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

# Incorporate data
df = pd.read_csv('data/gapminder2007.csv')

# Initialize the app
app = Dash(
    external_stylesheets=[dbc.themes.CYBORG] # CYBORG theme  from dbc
)
server = app.server # initialize server

# App layout
app.layout = dbc.Container([ 
    html.H1(children='My First App with Data, Graph, and Controls'), # App TITLE
    
    html.Hr(), # Horizontal line
    
    html.Div(children = 'x axis'), # x axis label
    
    dbc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='column-options'), # RadioItems for x axis
   
    html.Hr(), # Horizontal line
    
    html.Div(children = 'y axis'), # y axis label
         
    dbc.RadioItems(options = ['pop', 'lifeExp', 'gdpPercap'], value = 'gdpPercap', id='column-options2'), # RadioItems for y axis
    
    dbc.Button('Submit', id='submit-button', n_clicks=0), # Submit button, needed to update the graph
    
    dbc.Alert(id = 'app_alert', is_open = False, duration = 3000, children = 'X and Y axis must be different!'), # Alert message for 3 seconds if x and y axis are the same

    dcc.Graph(figure={}, id='graph1') # Empty graph to be updates with the callback function
])

# Add controls to build the interaction
@callback(
    Output(component_id='graph1', component_property='figure'), # Output to update the graph
    Output('app_alert', 'is_open'), # Output to show the alert message if needed
    Input('submit-button', 'n_clicks'), # Input to trigger the callback
    State(component_id='column-options', component_property='value'), # State to get the value of the x axis
    State(component_id='column-options2', component_property='value'), # State to get the value of the y axis
    prevent_initial_call=True # Prevent the callback to run at the beginning
)
def update_graph(sub_btn ,col_chosen, col_chosen2): # State and Inputs are passed as arguments
    if col_chosen == col_chosen2: # If x and y axis are the same
        return no_update, True # Do not graph the chhart and show the alert message
    else:
        fig = px.scatter(df, x = col_chosen, y = col_chosen2, color='continent') # Create the scatter plot
        return fig, no_update # Return the figure and do not show the alert message


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
