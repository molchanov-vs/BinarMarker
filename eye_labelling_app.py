import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import os
import base64
import json
import datetime

app = dash.Dash(__name__)

image_folder = '/Users/molchanov/dev/eye_labelling/EyesDataset'  # Update with the path to your image folder
image_list = sorted(os.listdir(image_folder))[:]
current_index = 0
results = {}

app.layout = html.Div([
    html.H1("Image Viewer"),
    html.Button('Previous', id='previous-button', n_clicks=0, style={'margin': '10px'}),
    html.Button('Next', id='next-button', n_clicks=0, style={'margin': '10px'}),
    html.Button('Opened', id='opened-button', n_clicks=0, style={'margin': '10px'}),
    html.Button('Closed', id='closed-button', n_clicks=0, style={'margin': '10px'}),
    html.Button('Save', id='save-button', n_clicks=0, style={'margin': '10px'}),
    html.Div(id='image-info', style={'margin': '10px'}),
    html.Div(id='output-image') # style={'margin': '10px'}
])


def parse_contents(image_path):
    encoded_image = base64.b64encode(open(image_path, 'rb').read())
    src_name = f'data:image/jpg;base64,{encoded_image.decode()}'
    return html.Div([
        html.Img(src=src_name, style={'width': '20%'}),
        html.H2(image_list[current_index])
    ])

@app.callback(
    Output('output-image', 'children'),
    [Input('previous-button', 'n_clicks'),
     Input('next-button', 'n_clicks'), 
     Input('opened-button', 'n_clicks'), 
     Input('closed-button', 'n_clicks'),
     Input('save-button', 'n_clicks')]
)
def update_output(previous_clicks, next_clicks, opened_click, closed_click, save_click):
    global current_index
    global results

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    if 'previous-button' in changed_id:
        current_index = (current_index - 1) % len(image_list)
    elif 'next-button' in changed_id:
        current_index = (current_index + 1) % len(image_list)
    elif 'opened-button' in changed_id:
        results[image_list[current_index]] = 1
        current_index = (current_index + 1) % len(image_list)
    elif 'closed-button' in changed_id:
        results[image_list[current_index]] = 0
        current_index = (current_index + 1) % len(image_list)
    elif 'save-button' in changed_id:
        save_json(results)
        
    image_path = os.path.join(image_folder, image_list[current_index])
    return parse_contents(image_path)

def save_json(data):
    json_path = '/Users/molchanov/dev/eye_labelling/json'
    with open(f'{json_path }/{get_current_date()}.json', "w") as json_file:
    # Write the dictionary as JSON data
        json.dump(data, json_file)

def get_current_date():
    # Get the current date
    current_date = datetime.datetime.now().date()
    
    # Convert the date to a string
    date_str = str(current_date)
    
    return date_str

if __name__ == '__main__':
    app.run_server(debug=True)
