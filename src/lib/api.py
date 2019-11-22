# -*- coding: utf-8 -*-

# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from lib import util
from lib import yt_api_util

class Channel:
    def __init__(self, item):
        self.id = item.get('id')
        self.title = item.get('snippet').get('localized').get('title')
        self.playlist = item.get('contentDetails').get('relatedPlaylists').get('uploads')

class SimpleVideo:
    def __init__(self, item):
        snippet = item.get('snippet')
        self.id = snippet.get('resourceId').get('videoId')
        self.title = snippet.get('title')

        localized = [snippet.get("localized", {}).get(key, "") for key in ["title", "description"]] 
        self.metadata = snippet.get('tags', [])\
            + [snippet.get(key, "") for key in ["title", "description"]]
        if localized:
            self.metadata += localized

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

    def fetch_videos(self, ids, batch_size = 10):
        result = {}
        batches = util.chunks(ids, batch_size)
        for batch in batches:
            response = self.fetch(','.join(batch))
            data = self.save_videos(response)
            result.update(data)
        return result

    def save_videos(self, response):
        data = {}
        for item in response.get('items'):
            id = item["id"]
            file_path = util.get_cache_json_path(id)
            with open(file_path, "w") as outfile:
                print("Write to %s" % outfile.name)
                json.dump(item, outfile)
                data[id] = yt_api_util.read_single_video_obj(item)
        return data

    def fetch_channels(self, ids):
        batches = util.chunks(ids, 30)
        results = []
        for batch in batches:
            request = self.get_youtube().channels().list(
                part="snippet,contentDetails",
                id=','.join(batch),
            )
            response = request.execute()
            results += [Channel(item) for item in response.get('items')]
        return results

    def fetch_playlist(self, id, max_result):
        request = self.get_youtube().playlistItems().list(
            part="snippet",
            playlistId=id,
            maxResults=max_result,
        )
        response = request.execute()
        return [SimpleVideo(item) for item in response.get('items')]

    def create_playlist(self, title, description):
        request = self.get_youtube().playlists().insert(
            part="snippet,status",
            body={
              "snippet": {
                "title": title,
                "description": description,
                "tags": [
                  "sparkar", "spark ar",
                ],
                "defaultLanguage": "en"
              },
              "status": {
                "privacyStatus": "private"
              }
            }
        )
        response = request.execute()
        print(response)
        print("id: %s" % response.get('id'))

    def add_video_to_playlist(self, playlist_id, position, video_id):
        request = self.get_youtube().playlistItems().insert(
            part="snippet",
            body={
              "snippet": {
                "playlistId": playlist_id,
                "position": position,
                "resourceId": {
                  "kind": "youtube#video",
                  "videoId": video_id,
                }
              }
            }
        )
        response = request.execute()
