import json
import sys
import argparse

import config
from lib.const import *
from lib.api import ApiDataLoader
from lib.data_loader import load_site_config

def get_video_id(item):
    return item['id']['videoId']

def fetch_single(channel_id, keyword="spark", max_result=30):
    data_loader = ApiDataLoader(config.DEVELOPER_KEY)
    response = data_loader.list_channel(channel_id, keyword, max_result)
    for item in response['items']:
        # exclude playlist
        if item['id']['kind'] == "youtube#video":
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            print("%s // %s" % (video_id, title))

def fetch_all():
    site = load_site_config(config.DEVELOPER_KEY)
    channels = set([(v[CHANNEL_ID], v[CHANNEL_TITLE]) for v in site.video_data.values()])
    for channel in channels:
        print("# %s" % channel[1])
        fetch_single(channel[0], max_result=5)
        print()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Search video in channel')
    parser.add_argument('--id', type=str)
    parser.add_argument('--keyword', '-k', type=str)
    parser.add_argument('--max', '-m', type=int)
    args = parser.parse_args()
    args = vars(args)

    if args['id'] is None:
        fetch_all()
    else:
        fetch_single(args['id'], keyword = args['keyword'], max_result = args['max'])
