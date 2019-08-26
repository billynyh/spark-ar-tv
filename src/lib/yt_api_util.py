import json

from lib import text_util
from lib.const import *

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

    title = snippet["title"]
    thumbnail_url = snippet["thumbnails"]["high"]["url"]
    channel_id = snippet["channelId"]
    channel_title = snippet["channelTitle"]
    raw_published_at = snippet["publishedAt"]
    raw_duration = content_details["duration"]
    view_count = stat["viewCount"]

    published_at = text_util.formate_date(raw_published_at)
    duration = text_util.format_duration(raw_duration)
   
    return {
      ID: id,
      TITLE: title,
      THUMBNAIL_URL: thumbnail_url,
      CHANNEL_ID: channel_id,
      CHANNEL_TITLE: channel_title,
      DURATION: duration,
      VIEW_COUNT: view_count,
      PUBLISHED_AT: published_at,
    }
