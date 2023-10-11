import requests

API_KEY = 'AIzaSyAwtFbRyaMZoIRMeI5wnyIdMJBXoiomZew'
SEARCH_ENGINE = '02efd5b6acd5442c6'

url = 'https://www.googleapis.com/customsearch/v1'

def search(query):
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE,
        'q': query
    }
    response = requests.get(url, params=params)
    return response.json()['items']
    
