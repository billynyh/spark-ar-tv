import json
import sys
import argparse

from site_config import DEVELOPER_KEY, LOCAL_CONFIG
from lib.api import ApiDataLoader
from lib.data_loader import load_site_data, load_skip_ids

class Item:
    def __init__(self, id, title):
        self.id = id
        self.title = title


def get_video_id(item):
    return item['id']['videoId']

def fetch_single_channel(channel_id, all_ids, skip_ids, new_only, keyword="spark", max_result=30):
    api = ApiDataLoader(DEVELOPER_KEY)
    response = api.list_channel(channel_id, keyword, max_result)
    result = []
    for item in response['items']:
        # exclude playlist
        if item['id']['kind'] == "youtube#video":
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            if new_only and video_id in all_ids:
                continue
            if video_id in skip_ids:
                continue
            data = Item(video_id, title)
            result.append(data)
    return result

def fetch_all(config, new_only = True, keyword="spark", max_result=10):
    site = load_site_data(config, DEVELOPER_KEY)
    all_ids = set(site.video_data.keys())
    skip_ids = set(load_skip_ids(config))
    channels = set([(v.channel_id, v.channel_title) for v in site.video_data.values()])
    result = []
    for channel in channels:
        print("Fetching %s..." % channel[1])
        items = fetch_single_channel(channel[0], all_ids, skip_ids, new_only, max_result=max_result)
        if len(items) > 0:
            result.append((channel[1], items))
    
    if len(result) == 0:
        print("No new data")
        return

    for v in result:
        print("# %s" % v[0])
        for item in v[1]:
            print("%s // %s" % (item.id, item.title))
        print()

def list_channels(config):
    site = load_site_data(config)
    channels = dict([(v.channel_id, v.channel_title) for v in site.video_data.values()])
    for id,title in channels.items():
        print("%s # %s" % (id, title))


def main():
    parser = argparse.ArgumentParser(description='Search video in channel')
    parser.add_argument('--id', type=str)
    parser.add_argument('--keyword', '-k', type=str)
    parser.add_argument('--max', '-m', type=int)
    args = parser.parse_args()

    if args.id is None:
        fetch_all(LOCAL_CONFIG, keyword = args.keyword, max_result = args.max)
    else:
        fetch_single(args.id, keyword = args.keyword, max_result = args.max)

if __name__=="__main__":
    main()
