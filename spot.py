import requests
import base64
import pandas as pd

# Spotify API credentials
client_id = 'ef77c32c837f4fbeaaeb34c2f5e17eb5'
client_secret = '778ea7e99f3549b5a4d8425de8ac5a5b'


# Encode credentials for Basic Authorization
credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# Get access token
token_url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": f"Basic {encoded_credentials}"
}
data = {
    "grant_type": "client_credentials"
}

response = requests.post(token_url, headers=headers, data=data)
access_token = response.json()['access_token']

# Define the API base URL and headers
base_url = "https://api.spotify.com/v1"
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Load your Excel file
excel_file_path = r'C:\Users\AISHWARYA\Documents\New folder\spotifyy.xlsx'
spotify_df = pd.read_excel(excel_file_path)

# Inspect the columns of the dataframe to identify track and artist name columns
print("Columns in the dataframe:", spotify_df.columns)

# Assuming the columns are 'track_name' and 'artist_name'
# Update these variables to match the actual column names in your dataset
track_name_col = 'track_name'
artist_name_col = 'artist(s)_name'

# Function to get album cover URL for a track
def get_album_cover_url(track_name, artist_name):
    query = f"track:{track_name} artist:{artist_name}"
    search_url = f"{base_url}/search"
    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }
    response = requests.get(search_url, headers=headers, params=params)
    results = response.json().get('tracks', {}).get('items', [])
    if results:
        album_cover_url = results[0]['album']['images'][0]['url']
        return album_cover_url
    return None

# Populate the 'urls' column
spotify_df['urls'] = spotify_df.apply(
    lambda row: get_album_cover_url(row[track_name_col], row[artist_name_col]),
    axis=1
)

# Save the updated dataframe to the same Excel file
spotify_df.to_excel(excel_file_path, index=False)

print("URLs added and Excel file updated successfully!")
