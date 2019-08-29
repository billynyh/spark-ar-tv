# -*- coding: utf-8 -*-

# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from lib import util
from lib import yt_api_util

class ApiDataLoader:

    def __init__(self, key):
        self.key = key

    def get_youtube(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=self.key)

        return youtube

    def fetch(self, ids):
        print("Start fetch %s" % ids)
        request = self.get_youtube().videos().list(
            part="snippet,contentDetails,statistics",
            id=ids
        )
        response = request.execute()
        return response

    def fetch_all(self, ids, batch_size = 10):
        result = {}
        batches = util.chunks(ids, batch_size)
        for batch in batches:
            response = self.fetch(','.join(batch))
            data = self.save(response)
            result.update(data)
        return result

    def save(self, response):
        data = {}
        for item in response.get('items'):
            id = item["id"]
            file_path = util.get_cache_json_path(id)
            with open(file_path, "w") as outfile:
                print("Write to %s" % outfile.name)
                json.dump(item, outfile)
                data[id] = yt_api_util.read_single_video_obj(item)
        return data

    def list_channel(self, id, keyword="spark", max_result=30):
        request = self.get_youtube().search().list(
            part="snippet",
            channelId=id,
            q=keyword,
            order="date",
            maxResults=max_result,
        )
        response = request.execute()
        return response
