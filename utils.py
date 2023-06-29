import json
import datetime


def save_json(data):
    json_path = '/Users/molchanov/dev/eye_labelling/json'
    with open(f'{json_path }/{get_current_date()}.json', "w") as json_file:
    # Write the dictionary as JSON data
        json.dump(data, json_file, indent=4)

def read_json(file_path):
    # Open the JSON file in read mode
    with open(file_path, "r") as json_file:
        # Load the JSON data from the file
        data = json.load(json_file)
    
    return data

def get_current_date():
    # Get the current date
    current_date = datetime.datetime.now()
    
    # Convert the date to a string
    date_str = str(current_date)
    
    return date_str