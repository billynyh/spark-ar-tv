import json
import sys
import argparse

import config_factory
from cleanup import cleanup
from site_config import DEVELOPER_KEY
from lib.api import ApiDataLoader
from lib.data_loader import *

def get_video_id(item):
    return item['id']['videoId']

def filter_videos(items, known_ids, keywords):
    result = []
    keywords = [k.lower() for k in keywords]
    for item in items:
        if item.id in known_ids:
            continue
        keep = False
        for s in item.metadata:
            for k in keywords:
                if k in s.lower():
                    keep = True
        if keep:
            result.append(item)
    return result

def fetch_single(config, master, channel_id):
    api = ApiDataLoader(DEVELOPER_KEY)
    channel_data = api.fetch_channels([channel_id])
    for c in channel_data:
        items = api.fetch_playlist(c.playlist, max_result=30)
        print(len(items))
        items = filter_videos(items, [], keywords=['spark', 'mask', 'sparkar'])
        print(len(items))
        for item in items:
            print("%s // %s" % (item.id, item.title))

def fetch_all(config, master, lang, new_only = True, max_result=10, single_channel_id = None):
    api = ApiDataLoader(DEVELOPER_KEY)

    data_dir = "data/%s" % lang
    site = master.lang_sites[lang]
    all_ids = set(site.video_data.keys())
    skip_ids = set(load_skip_ids(data_dir))
    channels = set([(v.channel_id, v.channel_title) for v in site.video_data.values()])
    result = []

    cache = load_cache()

    print("Fetching channels...")
    channel_ids = set([c[0] for c in channels])
    if single_channel_id:
        if single_channel_id in channel_ids:
            channel_ids = [single_channel_id]
        else:
            channel_ids = []
    channel_data = api.fetch_channels(list(channel_ids))
    for c in channel_data:
        print("Fetching %s(%s)..." % (c.title, c.playlist))
        items = api.fetch_playlist(c.playlist, max_result=max_result)
        items = filter_videos(items, all_ids.union(skip_ids), keywords=['spark', 'mask', 'sparkar'])
        if len(items) > 0:
            result.append((c.title, items, c.id))
    
    if len(result) == 0:
        print("No new data")
        return master

    for v in result:
        print("# %s" % v[0])
        for item in v[1]:
            print("%s // %s" % (item.id, item.title))
        print()

    for v in result:
        for g in site.groups:
            channel_id = site.video_data[g.ids[0]].channel_id
            if channel_id == v[2]:
                for item in v[1]:
                    g.ids.append(item.id)
    # Reload video data
    all_youtube_ids = [id for g in site.groups for id in g.ids]
    site.video_data = load_video_data(all_youtube_ids, cache, config.api_key)
    return master

def main():
    parser = argparse.ArgumentParser(description='Search video in channel')
    parser.add_argument('--id', type=str)
    parser.add_argument('--max', '-m', type=int, default=10)
    parser.add_argument('--cleanup', action='store_true')
    args = parser.parse_args()

    config = config_factory.load()
    master = master_site(config, merge_small_groups = False)

    if args.cleanup:
        cleanup(master)
        return

    skip_lang = ['fr']
    langs = config.site_config.languages
    for lang in langs:
        if lang in skip_lang:
            print("Skip fetching %s" % lang)
            continue
        print("==== Fetching %s ====" % lang)
        master = fetch_all(config, master, lang, max_result = args.max, single_channel_id = args.id)
    cleanup(master)

if __name__=="__main__":
    main()
