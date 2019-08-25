import json
import sys
import argparse

import api

def get_video_id(item):
    return item['id']['videoId']

def fetch(channel_id, keyword="spark", max_result=30):
    response = api.list_channel(channel_id, keyword, max_result)
    for item in response['items']:
        # exclude playlist
        if item['id']['kind'] == "youtube#video":
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            print("%s // %s" % (video_id, title))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Search video in channel')
    parser.add_argument('id', type=str)
    parser.add_argument('--keyword', '-k', type=str)
    parser.add_argument('--max', '-m', type=int)
    args = parser.parse_args()
    args = vars(args)

    fetch(args['id'], keyword = args['keyword'], max_result = args['max'])
