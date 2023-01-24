import pandas as pd
import re
from ast import literal_eval
from general import youtube
from typing import Union

FORMULA_1_CHANNEL = 'UCB_qr75-ydFVKSF9Dmo6izg'

def get_highlight_video_from_playlist(id):
    request = youtube.playlistItems().list(
        part = 'contentDetails, snippet',
        playlistId = id,
        maxResults = 50
    )
    good_videos = []
    response = request.execute()
    for item in response['items']:
        if 'Race Highlights' in item['snippet']['title']:
            good_video = {
                'id': item['contentDetails']['videoId'],
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['high'],
            }
            good_videos.append(good_video)
    return good_videos

def get_playlists(channel_id, next_page_token):
    request = youtube.playlists().list(
        part = 'contentDetails, snippet',
        channelId = channel_id,
        maxResults = 30,
        pageToken = next_page_token,
    )
    response = request.execute()
    next_page_token = response.get('nextPageToken')
    playlists_id = []
    for item in response['items']:
        playlists_id.append(item['id'])
    return playlists_id, next_page_token

def get_playlist_length_info(channel_id, next_page_token):
    request = youtube.playlists().list(
        part = 'contentDetails, snippet',
        channelId = channel_id,
        maxResults = 30,
        pageToken = next_page_token,
    )
    response = request.execute()
    next_page_token = response.get('nextPageToken')
    playlists_info = []
    for item in response['items']:
        playlists_info.append({
            'id': item['id'],
            'count_item': item['contentDetails']['itemCount'],
            'title': item['snippet']['title'],
        })
    return playlists_info, next_page_token
    
def get_video_details(id):
    request = youtube.videos().list(
        part = "contentDetails, id, liveStreamingDetails, localizations, player, recordingDetails, snippet, statistics, status, topicDetails",
        id = id
    )
    return request.execute()

def show_playlists_length(channel_id):
    dict_info = []
    while True:
        next_page_token = None
        playlists, next_page_token = get_playlist_length_info(channel_id, next_page_token)
        dict_info += playlists
        if not next_page_token:
            break
    print(*dict_info, sep="\n")

def get_all_playlists_id(channel_id):
    result = []
    while True:
        next_page_token = None
        playlists, next_page_token = get_playlists(channel_id, next_page_token)
        result += playlists
        if not next_page_token:
            break
    return result

def get_race_highlights(playlists_id: list) -> list:
    good_videos = []
    for playlist_id in playlists_id: # works only assuming each playlist has desired videos in the first 50 videos
        good_videos += get_highlight_video_from_playlist(playlist_id)  
    return good_videos

def get_all_race_highlights():
    return get_race_highlights(get_all_playlists_id(FORMULA_1_CHANNEL))

######

def get_year_full_name(name: str) -> str:
    pattern = "(70th .* Grand Prix|[0-9]{4} .* Grand Prix)"
    matches = re.findall(pattern, name)
    if len(matches) > 0:
        return matches[0]
    else: return None

def unify_grand_prix_name(grand_prix_name):
    replacements = {
        'Sao Paulo Grand Prix': 'Brazilian Grand Prix', 
        'Brazil Grand Prix': 'Brazilian Grand Prix',
        'Mexico City Grand Prix': 'Mexican Grand Prix', 
        'Mexico Grand Prix': 'Mexican Grand Prix',
        'US Grand Prix': 'United States Grand Prix',
    }
    replaced_name = replacements.get(grand_prix_name)
    return replaced_name if replaced_name else grand_prix_name

def get_year_from_grand_prix_title(title: str) -> int:
    if title == '70th Anniversary Grand Prix':
        return 2020
    else: return (int)(re.findall("[0-9]{4}", title)[0])
    
def get_full_name_from_grand_prix_title(title: str) -> str:
    if title == '70th Anniversary Grand Prix':
        return title[5:]
    return re.split("[0-9]{4} ", title)[1]
    
def add_url_prefix(name: str) -> str:
    return 'https://www.youtube.com/watch?v=' + name

def get_cleaned_video_data(source: Union[str, list]) -> pd.DataFrame:
    if type(source) == str:
        with open(source) as f:
            data = f.readlines()
            data = [literal_eval(x.strip()) for x in data]
    else: data = source
    for item in data:
        item['thumbnail'] = item['thumbnail']['url']
    data = pd.DataFrame(data)
    data = data.drop_duplicates()
    pattern = ".*(Formula 2|Formula 3|F2|F3|W Series|Virtual|Extended|Esports|FORMULA 1).*"
    filter = data['title'].str.match(pattern)
    data = data[~filter]
    data['title'] = data['title'].apply(get_year_full_name)
    data['year'] = data['title'].apply(get_year_from_grand_prix_title)
    data['full_name'] = data['title'].apply(get_full_name_from_grand_prix_title)
    data['full_name'] = data['full_name'].apply(unify_grand_prix_name)
    data['id'] = data['id'].apply(add_url_prefix)
    data.rename(columns={'id': 'link'}, inplace=True)
    data.drop(columns=['title'], inplace=True)
    return data