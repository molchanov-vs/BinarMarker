import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import os
import base64

app = dash.Dash(__name__)

image_folder = '/Users/molchanov/dev/eye_labelling/EyesDataset'  # Update with the path to your image folder
image_list = sorted(os.listdir(image_folder))
current_index = 0

app.layout = html.Div([
    html.H1("Image Viewer"),
    html.Button('Previous', id='previous-button', n_clicks=0, style={'margin': '10px'}),
    html.Button('Next', id='next-button', n_clicks=0, style={'margin': '10px'}),
    html.Div(id='image-info', style={'margin': '10px'}),
    html.Div(id='output-image') # style={'margin': '10px'}
])


def parse_contents(image_path):
    encoded_image = base64.b64encode(open(image_path, 'rb').read())
    src_name = f'data:image/jpg;base64,{encoded_image.decode()}'
    return html.Div([
        html.Img(src=src_name, style={'width': '10%'}),
        html.H2(image_list[current_index])
    ])

@app.callback(
    Output('output-image', 'children'),
    [Input('previous-button', 'n_clicks'),
     Input('next-button', 'n_clicks')]
)
def update_output(previous_clicks, next_clicks):
    global current_index

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    if 'previous-button' in changed_id:
        current_index = (current_index - 1) % len(image_list)
    elif 'next-button' in changed_id:
        current_index = (current_index + 1) % len(image_list)

    image_path = os.path.join(image_folder, image_list[current_index])
    return parse_contents(image_path)

if __name__ == '__main__':
    app.run_server(debug=True)
