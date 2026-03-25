import requests
from datetime import datetime

API_KEY = "YOUR_API_KEY"
CHANNEL_ID = "UCiGyWN6DEbnj2alu7iapuKQ"

def get_channel_data(API_KEY, CHANNEL_ID):
    try:    
        url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails&id={CHANNEL_ID}&key={API_KEY}"
        response = requests.get(url).json()

        data = response['items'][0]

        title = data['snippet']['title']
        description = data['snippet']['description']
        subs = int(data['statistics']['subscriberCount'])
        views = int(data['statistics']['viewCount'])
        videos = int(data['statistics']['videoCount'])

        uploads_playlist = data['contentDetails']['relatedPlaylists']['uploads']

        return {
            "Title": title,
            "Description": description,
            "Subscribers": f"{subs:,}",
            "Total Views": f"{views:,}",
            "Total Videos": f"{videos:,}",
            "Uploads Playlist": uploads_playlist
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}
    except (KeyError, IndexError) as e:
        return {"error": "Invalid response or channel not found"}

def get_latest_video_date(API_KEY, PLAYLIST_ID):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=1&playlistId={PLAYLIST_ID}&key={API_KEY}"
    response = requests.get(url).json()

    try:
        video = response['items'][0]
        published_at = video['snippet']['publishedAt']
        return datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%d %b %Y")
    except:
        return "Unknown"

channel_info = get_channel_data(API_KEY, CHANNEL_ID)

if "error" in channel_info:
    print("Error:", channel_info["error"])
else:
    latest_video_date = get_latest_video_date(API_KEY, channel_info["Uploads Playlist"])

    print("\n📺 Channel Summary")
    print("--------------------------")
    print(f"Title           : {channel_info['Title']}")
    print(f"Description     : {channel_info['Description'][:100]}...")
    print(f"Subscribers     : {channel_info['Subscribers']}")
    print(f"Total Views     : {channel_info['Total Views']}")
    print(f"Total Videos    : {channel_info['Total Videos']}")
    print(f"Last Upload Date: {latest_video_date}")
