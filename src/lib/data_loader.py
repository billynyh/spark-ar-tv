import datetime

from lib.api import ApiDataLoader
from lib.const import *
from lib.model import SiteConfig
from lib import util
from lib import yt_api_util

# parse data.txt
def parse(file_path):
    print("Parsing %s" % file_path)
    f = open(file_path)
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
    
def process_groups(groups, video_data):
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

    # sort each group by publish date
    for group in result:
        group[LIST] = sort_video_ids_by_time(group[LIST], video_data)
    
    return result

def sort_video_ids_by_time(ids, video_data):
    return sorted(
        ids,
        key=lambda id: video_data[id][PUBLISHED_AT], 
        reverse=True)

def load_cache():
    cache_files = util.get_cache_files()
    data = {}
    for id in cache_files:
        file_path = util.get_cache_path(id)
        data[id] = yt_api_util.read_single_video_json(file_path)
    return data

def load_video_data(ids, api_key):
    print("Load video data")
    data = load_cache()
    need_fetch = [id for id in ids if not id in data.keys()]

    if len(need_fetch) > 0:
        print("Start fetching %s video data" % len(need_fetch))
        data_loader = ApiDataLoader(api_key)
        fetched_data = data_loader.fetch_all(need_fetch)
        data.update(fetched_data)
  
    return data

def filter_video_by_date(video_data, start_date, end_date):
    result = []
    for id,v in video_data.items():
        published_at = v[PUBLISHED_AT] 
        if start_date <= published_at and published_at < end_date:
            result.append(id)
    return sort_video_ids_by_time(result, video_data)

def group_by_time(video_data):
    dummy_start_date = datetime.date(2017, 7, 1)
    start_date = datetime.date(2019, 7, 1)
    today = datetime.date.today()
    week = datetime.timedelta(weeks=1)

    groups = [{
        TITLE: "Previous Videos",
        LIST: filter_video_by_date(video_data, dummy_start_date, start_date)
    }]

    while start_date <= today:
        end_date = start_date + week
        group = {
            TITLE: "Week %s" % start_date,
            LIST: filter_video_by_date(video_data, start_date, end_date)
        }
        
        if len(group[LIST]) > 0:
            groups.insert(0, group)
        start_date = end_date
    return groups

def load_site_config(api_key):
    groups = parse(DATA_FILE)
    most_viewed = parse(MOST_VIEWED_DATA_FILE)[0][LIST]
    latest = parse(LATEST_DATA_FILE)[0][LIST]

    all_youtube_ids = [id for g in groups for id in g[LIST]]
    print("Num of videos: %s" % len(all_youtube_ids))

    video_data = load_video_data(all_youtube_ids, api_key)

    # merge and sort
    groups = process_groups(groups, video_data)

    site = SiteConfig()
    site.groups = groups
    site.video_data = video_data
    site.most_viewed = most_viewed
    site.latest = latest
    site.groups_by_time = group_by_time(video_data)
    return site

def sort_videos(video_data):
    ids = video_data.keys()
    most_viewed = sorted(ids, key=lambda id: -int(video_data[id][VIEW_COUNT]))
    latest = sorted(ids, key=lambda id: video_data[id][PUBLISHED_AT], reverse=True)

    return (most_viewed, latest)