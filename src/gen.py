import pprint
import json
import shutil
import os.path

import api
import config
import html_helper
import util
from const import *

FILE = "data/data.txt"

# parse data.txt
def parse():
    print("Parsing %s" % FILE)
    f = open(FILE)
    groups = []
    current_group = None
    for s in f.readlines():
        s = s.strip()
        if not s:
            continue
        if s.startswith("#"):
            if current_group:
                groups.append(current_group)
            current_group = {}
            current_group[TITLE] = s[1:].strip()
            current_group[LIST] = []
            continue

        current_group[LIST].append(util.extract_youtube_id(s))
    if current_group: 
        groups.append(current_group)
        
    return groups
    
def merge_groups(groups):
    # merge all groups with less than 2 vid to Others
    result = []
    others = []
    for group in groups:
        if len(group[LIST]) <= 2:
            others += group[LIST]
        else:
            result.append(group)
    if len(others) > 0:
        result.append({TITLE: 'Others', LIST: others})
    return result

def load_video_data(ids):
    print("Load video data")
    data = {}
    need_fetch = []
    cache_files = util.get_cache_files()
    for id in ids:
        if id in cache_files:
            file_path = util.get_cache_path(id)
            data[id] = util.read_single_video_json(file_path)
        else:
            need_fetch.append(id)
    if len(need_fetch) > 0:
        print("Start fetching %s video data" % len(need_fetch))
        fetched_data = api.fetch_all(need_fetch)
        data.update(fetched_data)
  
    return data

def sort_videos():
    groups = parse()
    ids = [id for g in groups for id in g[LIST]]
    video_data = load_video_data(ids)
    most_viewed = sorted(ids, key=lambda id: -int(video_data[id][VIEW_COUNT]))
    latest = sorted(ids, key=lambda id: -int(video_data[id][PUBLISHED_AT]))

    return (mosted_vided, latest)

def main():
    fetch = True
    read_cache = True

    groups = parse()
    groups = merge_groups(groups)

    all_youtube_ids = [id for g in groups for id in g[LIST]]
    print("Num of videos: %s" % len(all_youtube_ids))

    video_data = load_video_data(all_youtube_ids)

    html = html_helper.gen_html(groups, video_data)
    with open("%s/index.html" % config.OUT_DIR, "w") as outfile:
        outfile.write(html)
        print("Generated %s" % outfile.name)
    util.copy_all("assets", config.OUT_ASSETS_DIR)
    
if __name__ == "__main__":
    main()
