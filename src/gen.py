import pprint
import json
import shutil
import os.path

import config
from lib import html_helper
from lib import util
from lib import yt_api_util
from lib.api import ApiDataLoader
from lib.data_loader import load_site_config
from lib.model import SiteConfig
from lib.const import *


def open_out_file(name):
    return open("%s/%s" % (config.OUT_DIR, name), "w")

def week_pages(site):
    pages = []
    for week in site.groups_by_time:
        if not week.title.startswith("Week "):
            continue
        path = "weeks/%s.html" % week.title[5:] 
        pages.append((path, html_helper.gen_week_html(site, week)))
    return pages

def main():
    util.prepare_cache()

    site = load_site_config(config.DEVELOPER_KEY)
    pages = [
        ("index.html", html_helper.gen_timeline_html(site)),
        ("debug.html", html_helper.gen_debug_html(site)),
        ("channels.html", html_helper.gen_channel_html(site)),
    ] + week_pages(site)

    for page in pages:
        with open_out_file(page[0]) as outfile:
            outfile.write(page[1])
            print("Generated %s" % outfile.name)

    # Copy assets
    util.copy_all("assets", config.OUT_ASSETS_DIR)
    
if __name__ == "__main__":
    main()
