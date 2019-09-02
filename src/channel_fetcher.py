import json
import sys
import argparse

import site_config
from site_config import DEVELOPER_KEY
from lib.api import ApiDataLoader
from lib.data_loader import load_site_data, load_skip_ids

class Item:
    def __init__(self, id, title):
        self.id = id
        self.title = title


def get_video_id(item):
    return item['id']['videoId']

def filter_videos(items, known_ids, keyword):
    result = []
    for item in items:
        if item.id in known_ids:
            continue
        if not keyword.lower() in item.title.lower():
            continue
        result.append(item)
    return result

def fetch_all(config, new_only = True, keyword="spark", max_result=10):
    api = ApiDataLoader(DEVELOPER_KEY)

    data_dir = "data/en"
    site = load_site_data(config, path=data_dir, api_key=DEVELOPER_KEY)
    all_ids = set(site.video_data.keys())
    skip_ids = set(load_skip_ids(data_dir))
    channels = set([(v.channel_id, v.channel_title) for v in site.video_data.values()])
    result = []

    print("Fetching channels...")
    channel_data = api.fetch_channels([c[0] for c in channels])
    for c in channel_data:
        print("Fetching %s(%s)..." % (c.title, c.playlist))
        items = api.fetch_playlist(c.playlist, max_result=max_result)
        items = filter_videos(items, all_ids.union(skip_ids), keyword)
        if len(items) > 0:
            result.append((c.title, items))
    
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

def facebook_playlist():
    ids = "PLb0IAmt7-GS3YTAnK4PkLCAuB1niVQKhy,PLb0IAmt7-GS3AIinKLd6_UO59uwxY_37i,PLb0IAmt7-GS23uF0mQ0T2pDSVnmpSRmmf".split(',')
    api = ApiDataLoader(DEVELOPER_KEY)
    result = []
    for id in ids:
        items = api.fetch_playlist(id, max_result=20)
        result.append((id, items))

    for v in result:
        print("# %s" % v[0])
        for item in v[1]:
            print("%s // %s" % (item.id, item.title))
        print()
    

def main():
    parser = argparse.ArgumentParser(description='Search video in channel')
    parser.add_argument('--id', type=str)
    parser.add_argument('--keyword', '-k', type=str, default="spark")
    parser.add_argument('--max', '-m', type=int, default=10)
    args = parser.parse_args()

    config = site_config.generator

    if args.id is None:
        fetch_all(config, keyword = args.keyword, max_result = args.max)
    else:
        print("TODO fetch single channel")

if __name__=="__main__":
    main()
    #facebook_playlist()
