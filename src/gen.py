import pprint
import json
import shutil
import os.path

import config
from lib import html_helper
from lib import util
from lib import yt_api_util
from lib.api import ApiDataLoader
from lib.data_loader import parse, load_video_data, process_groups
from lib.model import SiteConfig
from lib.const import *

DATA_FILE = "data/data.txt"
LATEST_DATA_FILE = "data/latest.txt"
MOST_VIEWED_DATA_FILE = "data/most_viewed.txt"

def load_site_config():
    groups = parse(DATA_FILE)
    most_viewed = parse(MOST_VIEWED_DATA_FILE)[0][LIST]
    latest = parse(LATEST_DATA_FILE)[0][LIST]

    all_youtube_ids = [id for g in groups for id in g[LIST]]
    print("Num of videos: %s" % len(all_youtube_ids))

    video_data = load_video_data(all_youtube_ids, config.DEVELOPER_KEY)

    # merge and sort
    groups = process_groups(groups, video_data)

    site = SiteConfig()
    site.groups = groups
    site.video_data = video_data
    site.most_viewed = most_viewed
    site.latest = latest
    return site

def open_out_file(name):
    return open("%s/%s" % (config.OUT_DIR, name), "w")

def main():
    site = load_site_config()

    html = html_helper.gen_html(site)
    with open_out_file("index.html") as outfile:
        outfile.write(html)
        print("Generated %s" % outfile.name)
    with open_out_file("debug.html") as outfile:
        outfile.write(html)
        print("Generated %s" % outfile.name)
    util.copy_all("assets", config.OUT_ASSETS_DIR)
    
if __name__ == "__main__":
    main()
