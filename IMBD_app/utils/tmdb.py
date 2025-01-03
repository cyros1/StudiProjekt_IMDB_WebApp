import requests
from django.conf import settings

BASE_URL = "https://api.themoviedb.org/3"
API_KEY = "2af4d814ca966334015aa4ea035219e7"

def fetch_tmdb_data(endpoint, params=None):
    """
    Fetch data from TMDb API.
    :param endpoint: API endpoint (e.g., 'movie/popular', 'search/movie').
    :param params: Dictionary of additional parameters.
    :return: JSON response or None if the request fails.
    """
    if params is None:
        params = {}

    params['api_key'] = API_KEY
    url = f"{BASE_URL}/{endpoint}"

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching TMDb data: {response.status_code}")
        return None

