import datetime
import os

from lib.api import ApiDataLoader
from lib.model import MasterSite, Site, Group, ChannelList
from lib import util
from lib import yt_api_util
from lib.path_util import PathHelper
from lib.nav_helper import CHANNEL_LIST_DISPLAY_NAME
from multiprocessing import Pool
from time import perf_counter 

# parse data.txt
def parse(file_path):
    if not os.path.exists(file_path):
        return []
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
            current_group = Group(title = s[1:].strip(), ids = [])
            continue

        current_group.ids.append(util.extract_youtube_id(s))
    if current_group: 
        groups.append(current_group)
        
    return groups
 
def parse_skip_file(file_path):
    if not os.path.exists(file_path):
        return []
    f = open(file_path)
    return [util.extract_youtube_id(line.strip()) for line in f.readlines() if line.strip()]

def process_groups(groups, video_data, merge_small_groups = True):
    # merge all groups with less than 2 vid to Others
    result = []
    others = []
    group_map = {}
    for group in groups:
        g_id = video_data[group.ids[0]].channel_id
        if group_map.get(g_id, None):
            group_map[g_id].ids += group.ids
        else:
            group_map[g_id] = group
    groups = group_map.values()

    for group in groups:
        if merge_small_groups and len(group.ids) <= 2:
            others += group.ids
        else:
            result.append(group)
    
    result = sorted(result, key = lambda g: g.title.upper())
    if len(others) > 0:
        result.append(Group('Others', others))

    # sort each group by publish date
    for group in result:
        group.ids = sort_video_ids_by_time(group.ids, video_data)
        group.slug = video_data[group.ids[0]].channel_id

    return result

def load_fb_videos(path):
    f = open(path)
    return [s.split()[0] for s in f.readlines()]

def load_custom():
    # two lanes fb videos
    data = [
      {
        'title' : "Two Lane Social",
        'urls' : load_fb_videos("data/custom/two_lane.txt"),
        'slug' : "two-lane",
      }
    ]
    return data

def load_blogs():
    data = [
      {
        'title': '2019 Top 5 most viewed Spark AR youtube video',
        'slug': '20191231-top-5',
      }
    ]
    return data

def sort_video_ids_by_time(ids, video_data):
    return sorted(
        ids,
        key=lambda id: (video_data[id].published_at, video_data[id].channel_id, id), 
        reverse=True)

def load_cache():
    cache_files = util.get_cache_json_files()
    data = {}
    for id in cache_files:
        file_path = util.get_cache_json_path(id)
        data[id] = yt_api_util.read_single_video_json(file_path)
    return data


def load_video_data(ids, cache, api_key):
    st_time = perf_counter()
    print("Load video data")
    need_fetch = [id for id in ids if not id in cache.keys()]
    data = {id:cache[id] for id in ids if id in cache}

    if len(need_fetch) > 0:
        if api_key is None:
            print("Set api key to fetch data")
        else:
            print("Start fetching %s video data" % len(need_fetch))
            data_loader = ApiDataLoader(api_key)
            fetched_data = data_loader.fetch_videos(need_fetch)
            data.update(fetched_data)
    print("- end load video data, timespent %f" % (perf_counter() - st_time))
    return data

def filter_video_by_date(video_data, start_date, end_date):
    result = []
    for id,v in video_data.items():
        if start_date <= v.published_at and v.published_at < end_date:
            result.append(id)
    return sort_video_ids_by_time(result, video_data)

def group_by_week(video_data):
    dummy_start_date = datetime.date(2017, 7, 1)
    start_date = datetime.date(2019, 7, 1)
    tmr = datetime.date.today() + datetime.timedelta(days=1) # consider timezone
    week = datetime.timedelta(weeks=1)

    groups = []

    prev_videos = Group(
        "Previous Videos",
        filter_video_by_date(video_data, dummy_start_date, start_date)
    )
    if len(prev_videos.ids) > 0:
        groups += [prev_videos]

    while start_date <= tmr:
        end_date = start_date + week
        title = "Week %s" % start_date
        ids = filter_video_by_date(video_data, start_date, end_date)
        group = Group(title, ids) 

        if len(group.ids) > 0:
            groups.insert(0, group)
        start_date = end_date
    return groups

def sort_by_num_videos(groups):
    return sorted(groups, key = lambda group: -len(group.ids))

def load_site_data(config, path, video_cache, merge_small_groups = True):
    api_key = config.api_key
    ph = PathHelper(path)

    groups = parse(ph.get_data_file())
    most_viewed_data = parse(ph.get_most_viewed_data_file())
    latest_data = parse(ph.get_latest_data_file())

    if len(most_viewed_data) > 0:
        most_viewed = most_viewed_data[0].ids
    else:
        most_viewed = []

    if len(latest_data) > 0:
        latest = latest_data[0].ids
    else:
        latest = []

    all_youtube_ids = [id for g in groups for id in g.ids]
    print("Num of videos: %s" % len(all_youtube_ids))

    video_data = load_video_data(all_youtube_ids, video_cache, api_key)

    # merge and sort
    groups_by_num_videos = sort_by_num_videos(groups) 
    groups = process_groups(groups, video_data, merge_small_groups)

    site = Site()
    site.groups = groups
    site.video_data = video_data
    site.most_viewed = most_viewed
    site.latest = latest
    site.groups_by_week = group_by_week(video_data)
    site.groups_by_num_videos = groups_by_num_videos
    site.num_videos = len(all_youtube_ids)
    return site

def load_global_groups(config, video_cache):
    groups = []
    for lang in config.site_config.languages:
        ph = PathHelper("data/%s" % lang)
        groups += parse(ph.get_data_file())
    
    all_youtube_ids = [id for g in groups for id in g.ids]
    video_data = load_video_data(all_youtube_ids, video_cache, config.api_key)

    groups = process_groups(groups, video_data, False)
    return groups

def load_skip_ids(data_dir):
    ph = PathHelper(data_dir)
    return parse_skip_file(ph.get_skip_file())

def sort_videos(video_data):
    ids = video_data.keys()
    most_viewed = sorted(ids, key=lambda id: -int(video_data[id].view_count))
    latest = sorted(ids, key=lambda id: video_data[id].published_at, reverse=True)

    return (most_viewed, latest)


def single_lang_site(config, lang, video_cache, merge_small_groups = True):
    site = load_site_data(
        config, 
        "data/%s" % lang,
        video_cache,
        merge_small_groups = merge_small_groups)
    site.url = config.site_config.url
    site.site_config = config.site_config
    site.lang = lang
    return site

def global_site(config, video_cache):
    site = Site()
    site.video_data = None
    site.url = config.site_config.url
    site.site_config = config.site_config
    site.lang = "global"
    site.groups = load_global_groups(config, video_cache)
    site.groups_by_num_videos = sort_by_num_videos(site.groups)

    site.topics = parse("data/topics.txt")
    site.facebook = parse("data/facebook.txt")
    site.interviews = parse("data/interviews.txt")
    
    all_groups = site.groups + site.facebook + site.topics + site.interviews
    all_youtube_ids = set([id for g in all_groups for id in g.ids])
    site.video_data = load_video_data(all_youtube_ids, video_cache, config.api_key)
    site.groups_by_week = group_by_week(site.video_data)
    for topic in site.topics:
        topic.ids = sort_video_ids_by_time(topic.ids, site.video_data)
    for g in site.facebook:
        g.ids = sort_video_ids_by_time(g.ids, site.video_data)
    site.topics = sorted(site.topics, key=lambda topic: topic.title)

    site.custom = load_custom()
    site.blogs = load_blogs()
    site.gen_channel_html = True
    site.gen_sitemap = True
    site.gen_search = True
    return site

def master_site(config, merge_small_groups = True):
    master = MasterSite()
    api_key = config.api_key
    print(api_key)
    langs = config.site_config.languages
    video_cache = load_cache()
    sites = [single_lang_site(config, lang, video_cache, merge_small_groups) for lang in langs]
    for site in sites:
        master.lang_sites[site.lang] = site

    master.global_site = global_site(config, video_cache)
    master.global_site.most_viewed = master.lang_sites['en'].most_viewed
    master.config = config

    return master
