# -*- coding: utf-8 -*-

# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import config
import util
from const import *

from pprint import pprint

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def get_youtube():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=config.DEVELOPER_KEY)

    return youtube

def fetch(ids):
    print("Start fetch %s" % ids)
    request = get_youtube().videos().list(
        part="snippet,contentDetails,statistics",
        id=ids
    )
    response = request.execute()
    return response

def fetch_all(ids, batch_size = 10):
    result = {}
    batches = util.chunks(ids, batch_size)
    for batch in batches:
        response = fetch(','.join(batch))
        data = save(response)
        result.update(data)
    return result

def save(response):
    data = {}
    for item in response.get('items'):
        id = item["id"]
        file_path = util.get_cache_path(id)
        with open(file_path, "w") as outfile:
            print("Write to %s" % outfile.name)
            json.dump(item, outfile)
            data[id] = util.read_single_video_obj(item)
    return data

def list_channel(id, keyword="spark", max_result=30):
    request = get_youtube().search().list(
        part="snippet",
        channelId=id,
        q=keyword,
        order="date",
        maxResults=max_result,
    )
    response = request.execute()
    return response

def sample_fetch():
    id = "d789vqCo_-A"
    response = fetch(id)
    save(response)

def sample_list_channel():
    id = "UC3zmATtNhDuYOketH1zF5sw"
    response = list_channel(id, max_result=5)
    pprint(response)

if __name__ == "__main__":
    sample_list_channel()
