import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import os

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Image Labeling App'),
    dcc.Dropdown(
        id='image-dropdown',
        options=[{'label': filename, 'value': filename} for filename in os.listdir('/Users/molchanov/dev/eye_labelling/EyesDataset')],
        placeholder='Select an image'
    ),
    html.Img(id='image-display'),
    html.Button('Label as 1', id='button-1', n_clicks=0),
    html.Button('Label as 0', id='button-0', n_clicks=0)
])

@app.callback(
    Output('image-display', 'src'),
    Output('image-display', 'style'),
    Input('image-dropdown', 'value'),
    Input('button-1', 'n_clicks'),
    Input('button-0', 'n_clicks')
)
def update_image(image_filename, button_1_clicks, button_0_clicks):
    if image_filename:
        image_path = os.path.join('/Users/molchanov/dev/eye_labelling/EyesDataset', image_filename)
        if button_1_clicks > 0:
            # Process the label as 1 (save to file/database)
            print('Label: 1')
        elif button_0_clicks > 0:
            # Process the label as 0 (save to file/database)
            print('Label: 0')
        return image_path, {'display': 'block'}
    return '', {'display': 'none'}


@app.callback(
    Output('label-input', 'value'),
    Input('submit-button', 'n_clicks'),
    Input('label-input', 'value')
)
def submit_label(n_clicks, label):
    if n_clicks > 0:
        # Process the label (e.g., save it to a file/database)
        print(label)
        return ''
    return label


if __name__ == '__main__':
    app.run_server(debug=True)
