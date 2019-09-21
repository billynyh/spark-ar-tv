import json

from lib import text_util
from lib.model import Video

def read_api_data(f):
    data = json.load(open(f))
    result = {}
    for item in data["items"]:
        result[id] = read_single_video_obj(item)
    return result

def read_single_video_json(f):
    return read_single_video_obj(json.load(open(f)))

def read_single_video_obj(item):
    id = item["id"]
    snippet = item["snippet"]
    content_details = item["contentDetails"]
    stat = item["statistics"]
    raw_published_at = snippet["publishedAt"]
    raw_duration = content_details["duration"]

    video = Video()

    video.id = id
    video.title = snippet["title"]
    video.thumbnail_url = snippet["thumbnails"]["high"]["url"]
    video.channel_id = snippet["channelId"]
    video.channel_title = snippet["channelTitle"]
    video.view_count = stat["viewCount"]
    video.tags = snippet.get("tags", [])

    if snippet["thumbnails"].get("standard"):
        video.highres_thumbnail_url = snippet["thumbnails"]["standard"]["url"]
    elif snippet["thumbnails"].get("maxres"):
        video.highres_thumbnail_url = snippet["thumbnails"]["maxres"]["url"]
    else:
        video.highres_thumbnail_url = video.thumbnail_url

    video.published_at = text_util.formate_date(raw_published_at)
    video.raw_published_at = raw_published_at
    video.duration = text_util.format_duration(raw_duration)
    video.video_url = "https://youtube.com/watch?v=%s" % id
    video.channel_url = "https://www.youtube.com/channel/%s" % video.channel_id
   
    return video
