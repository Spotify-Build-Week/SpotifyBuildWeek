# import os
# import base64
# import requests
# import datetime
# from urllib.parse import urlencode
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# import pickle
# import numpy as np
# import pandas as pd
# import matplotlib as plt 
# from scipy.spatial import distance
# from models import model
# SPOTIFY_API_KEY = '7f15fad76ad8451aafb68fb31e761cdf'
# SPOTIFY_API_KEY_SECRET = '5ce5caec03d54549aebc1987db2a4023'
# redirect_uri = 'http://localhost:8888/callback'

# class SpotifyAPI(object):
#     access_token = None
#     access_token_expires = datetime.datetime.now()
#     access_token_did_expire = True
#     client_id = None
#     client_secret = None
#     token_url = 'https://accounts.spotify.com/api/token'
    
#     def __init__(self, client_id, client_secret, *args, **kwargs):
#         # Incase we want to inherit from somehwere else
#         super().__init__(*args, **kwargs)
#         self.client_id = client_id
#         self.client_secret = client_secret
        
#     def get_client_credentials(self):
#         '''
#         Returns a base64 encoded string
#         '''
#         client_id = self.client_id
#         client_secret = self.client_secret
#         if client_secret == None or client_id == None:
#             raise Exception('You must set client_id and client_secret')
#         client_creds = f'{client_id}:{client_secret}'
#         client_creds_b64 = base64.b64encode(client_creds.encode())
#         return client_creds_b64.decode()
    
#     def get_token_headers(self):
#         client_creds_b64 = self.get_client_credentials()
#         return {
#             'Authorization': f'Basic {client_creds_b64}'
#         }
    
#     def get_token_data(self):
#         return {
#             'grant_type': 'client_credentials'
#         }
    
#     def perform_auth(self):
#         token_url = self.token_url
#         token_data = self.get_token_data()
#         token_headers = self.get_token_headers()
#         r = requests.post(token_url, data=token_data, headers=token_headers)
#         if r.status_code not in range(200, 299):
#                 raise Exception('Could not authenticate client.')
#                 # return False 
#         data = r.json()
#         now = datetime.datetime.now()
#         access_token = data['access_token']
#         expires_in = data['expires_in']
#         expires = now + datetime.timedelta(seconds=expires_in)
#         self.access_token = access_token
#         self.access_token_expires = expires
#         access_token_did_expire = expires < now
#         return True
    
#     def get_access_token(self):
#         token = self.access_token
#         expires = self.access_token_expires
#         now = datetime.datetime.now()
#         if expires < now:
#             self.perform_auth()
#             return self.get_access_token()
#         elif token == None:
#             self.perform_auth()
#             return self.get_access_token()
#         return token
    
#     def get_resource_header(self):
#         access_token = self.get_access_token()
#         headers = {
#             'Authorization': f'Bearer {access_token}'
#         }
#         return headers
    
#     def get_resource(self, lookup_id, resource_type='albums', version='v1'):
#         endpoint = f'https://api.spotify.com/{version}/{resource_type}/{lookup_id}'
#         headers = self.get_resource_header()
#         r = requests.get(endpoint, headers=headers)
#         if r.status_code not in range(200, 299):
#             return {}
#         return r.json()
    
#     def get_album(self, _id):
#         return self.get_resource(_id, resource_type='albums')

#     def get_artist(self, _id):
#         return self.get_resource(_id, resource_type='artists')

    
#     def base_search(self, query_params):
#         headers = self.get_resource_header()
#         endpoint = 'https://api.spotify.com/v1/search'
#         lookup_url = f'{endpoint}?{query_params}'
#         resp = requests.get(lookup_url, headers=headers)
#         if resp.status_code not in range(200, 299):
#             return {}
#         return resp.json()
    
#     def search(self, query=None, operator=None, operator_query=None,search_type='artist'):
#         if query == None:
#             raise Exception('A query is required')
#         if isinstance(query, dict):
#             query = ' '.join([f'{k}:{v}' for k,v in query.items()])
#         query_params = urlencode({'q': query, 'type': search_type.lower()})
#         if operator != None and operator_query != None:
#             if operator.lower() == 'or' or operator.lower() == 'not':
#                 operate = operator.upper()
#                 if isinstance(operator_query, str):
#                     query = f'{query} {operator} {operator_query}'
#         print(query_params)
#         return self.base_search(query_params)

# # instantiate spotify API object
# SPOTIFY_API = SpotifyAPI(SPOTIFY_API_KEY, SPOTIFY_API_KEY_SECRET)

# # instantiate spotiPy API object (wrapper for spotify API)
# auth_manager = SpotifyClientCredentials(SPOTIFY_API_KEY, SPOTIFY_API_KEY_SECRET)
# SPOTIPY_API = spotipy.Spotify(auth_manager=auth_manager)


# def retrieve_spotify_ids(song_name, artist_name):
#     """Example: retrieve_spotify_id('superstition','stevie wonder')
#     returns '4N0TP4Rmj6QQezWV88ARNJ'
#     """
#     token = SPOTIFY_API.get_access_token()
#     song = SPOTIFY_API.search(
#         {'track':song_name, 'artist':artist_name}, search_type='track')
#     song_id = song['tracks']['items'][0]['id']
#     artist_id = song['tracks']['items'][0]['album']['artists'][0]['id']
    
#     return song_id, artist_id


# def suggest_ids(song_name, artist_name, orig_df, scaled_df):
#     orig_input = orig_df.loc[(orig_df['track_name'] == song_name) & (orig_df['artist_name'] == artist_name)]
#     scaled_input = scaled_df.loc[orig_input.index[0]]
#     reshaped_input = scaled_input.values.reshape(1, -1)
#     n_dist_, n_ind_ = model.kneighbors(reshaped_input)
#     output = orig_df[['track_name', 'artist_name']].loc[list(n_ind_[0][1:])]
#     return output

# def retrieve_audio_features(spotify_id):
#     """Example: retrieve_audio_features('4N0TP4Rmj6QQezWV88ARNJ')
#     returns a python dict
#     [{'danceability': 0.611,
#     'energy': 0.578,
#     'key': 1,
#     'loudness': -14.171,
#     'mode': 1,
#     'speechiness': 0.0676,
#     'acousticness': 0.0598,
#     'instrumentalness': 0.0219,
#     'liveness': 0.0983,
#     'valence': 0.884,
#     'tempo': 100.625,
#     'type': 'audio_features',
#     'id': '4N0TP4Rmj6QQezWV88ARNJ',
#     'uri': 'spotify:track:4N0TP4Rmj6QQezWV88ARNJ',
#     'track_href': 'https://api.spotify.com/v1/tracks/4N0TP4Rmj6QQezWV88ARNJ',
#     'analysis_url': 'https://api.spotify.com/v1/audio-analysis/4N0TP4Rmj6QQezWV88ARNJ',
#     'duration_ms': 266133,
#     'time_signature': 4}]"""    
#     audio_features = SPOTIPY_API.audio_features(tracks=[spotify_id])
#     return audio_features

# def retrieve_genres(artist_name):
#     """Example: retrieve_genre('stevie wonder')
#     returns ['funk', 'indie r&b', 'motown', 'quiet storm', 'soul']"""
#     artist = SPOTIFY_API.search({'artist':artist_name}, search_type='artist')
#     if (type(artist['artists']['items']) == list) & (len(artist['artists']['items'])>0):
#         genre_list = artist['artists']['items'][0]['genres']
#     else:
#         genre_list = []
#     return genre_list

# def spotipy_recs(spotify_id, limit=20):
#     """Example: spotipy_recs('4N0TP4Rmj6QQezWV88ARNJ', limit=3)
#     returns
#     [['6gJdDnF2TzfA1WPMXuCa3x', 'Proud Mary', 'Tina Turner'],
#     ['2DYtBXueUkZyUZAHKJAAIs', 'We Are Family - 2006 Remaster', 'Sister Sledge'],
#     ['00pGV4EInVd77cnOIwPTCv', "Papa's Got A Brand New Bag", 'James Brown']]
#     """
#     recs = SPOTIPY_API.recommendations(seed_tracks=[spotify_id], limit=limit)
#     rec_list = []
#     for i in range(len(recs['tracks'])):
#         song_id = recs['tracks'][i]['id']
#         song_name = recs['tracks'][i]['name']
#         artist_name = recs['tracks'][i]['artists'][0]['name']
#         rec_list.append([song_id,song_name,artist_name])
#     return rec_list