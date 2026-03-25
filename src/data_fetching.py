import requests
import pandas as pd
from api import get_channel_data
import isodate
import mysql.connector

API_KEY = "YOUR_API_KEY"
CHANNEL_ID = "UCiGyWN6DEbnj2alu7iapuKQ"

def convert_duration(duration_str):
    duration = isodate.parse_duration(duration_str)
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def video_ids(API_KEY,playlist_id):
    video_ids=[]
    base_url="https://www.googleapis.com/youtube/v3/playlistItems"
    next_page_token=None                                             #YouTube API returns maximum 50 videos per request.
                                                                     #So all videos cannot be fetched in one batch.
                                                                     #So YouTube sends next page token to fetch next batch

    while True:
        url=f"{base_url}?part=contentDetails&maxResults=50&playlistId={playlist_id}&key={API_KEY}"
        if next_page_token:
            url+=f"&pageToken={next_page_token}"

        response=requests.get(url).json()
        items=response.get("items",[])

        for item in items:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token=response.get("nextPageToken")
        if not next_page_token:
            break

    return video_ids

def video_stats(API_KEY,video_ids):
    stats=[]
    base_url="https://www.googleapis.com/youtube/v3/videos"

    for i in range(0,len(video_ids),50):
        batch=video_ids[i:i+50]
        ids=",".join(batch)
        url=f"{base_url}?part=snippet,statistics,contentDetails&id={ids}&key={API_KEY}"
        response=requests.get(url).json()

        for item in response.get("items",[]):
            snippet=item["snippet"]
            statistics=item["statistics"]
            content=item["contentDetails"]

            stats.append({
                "Video ID":item["id"],
                "Title":snippet["title"],
                "Published Date":snippet["publishedAt"][:10],
                "Views":int(statistics.get("viewCount",0)),
                "Likes":int(statistics.get("likeCount",0)),
                "Duration":convert_duration(content.get("duration","PY0M0s"))
                })
    return stats

if __name__ == "__main__":
    print("Fetching channel info...")
    channel_info=get_channel_data(API_KEY,CHANNEL_ID)

    if "error" in channel_info:
        print("Error: ",channel_info["error"])
    else:
        playlist_id=channel_info["Uploads Playlist"]
        print("Fetching video IDs from playlist...")
        video_ids=video_ids(API_KEY,playlist_id)
        print(f"Found {len(video_ids)} videos. Fetching stats...")
        video_stats=video_stats(API_KEY,video_ids)

        df=pd.DataFrame(video_stats)
        df.to_csv(r"C:\Users\354ak\OneDrive\Desktop\Python Implementations\Projects\Youtube Tracker\Data\pw_stats.csv",index=False)
        print("CSV file saved")

        MYSQL_CONFIG= {
            "host":"localhost",
            "user":"root",
            "password":"123321",
            "database":"youtube_db"
            }

        create_table_query="""
        CREATE TABLE IF NOT EXISTS pw_stats (
            video_id VARCHAR(20) PRIMARY KEY,
            title TEXT,
            published_Date DATE,
            views INT,
            likes INT,
            duration VARCHAR(20)
        ) """

        try:
            conn=mysql.connector.connect(**MYSQL_CONFIG)
            cursor=conn.cursor()
            cursor.execute(create_table_query)
            insert_query="""
            REPLACE INTO pw_stats
            (video_id, title, published_Date, views, likes, duration)
            VALUES(%s, %s, %s, %s, %s, %s) """

            for _,row in df.iterrows():
                cursor.execute(insert_query, (
                    row["Video ID"],
                    row["Title"],
                    row["Published Date"],
                    row["Views"],
                    row["Likes"],
                    row["Duration"]
                    ))

            conn.commit()
            cursor.close()
            conn.close()
            print("MySQL file updated successfully")

        except mysql.connector.Error as err:
            print(f"MYSQL Error: {err}")
