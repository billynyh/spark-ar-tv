import pprint
import json
import shutil
import os.path

import site_config
from lib import html_helper
from lib import util
from lib import yt_api_util
from lib.api import ApiDataLoader
from lib.data_loader import load_site_data
from lib.model import SiteConfig, PageConfig
from lib.const import *


def open_out_file(out_dir, name):
    return open("%s/%s" % (out_dir, name), "w")

def week_pages(site, config):
    pages = []
    for week in site.groups_by_time:
        path = util.week_page_path(week)
        page_config = PageConfig(
            title = "%s | Spark AR TV" % week.title,
            og_image = util.get_group_banner_url(config, week)
        )
        pages.append((path, html_helper.gen_week_html(site, page_config, week)))
    return pages

def gen_site(site, config):
    pages = [
        ("index.html", html_helper.gen_timeline_html(site)),
        ("debug.html", html_helper.gen_debug_html(site)),
        ("channels.html", html_helper.gen_channel_html(site)),
    ] + week_pages(site, config)

    for page in pages:
        with open_out_file(config.out_dir, page[0]) as outfile:
            outfile.write(page[1])
            print("Generated %s" % outfile.name)

    # Copy assets
    util.copy_all("assets", config.out_assets_dir)


def main(prod=False):
    util.prepare_cache()

    site = load_site_data(site_config.DEVELOPER_KEY)
    configs = [site_config.LOCAL_CONFIG]
    if prod:
        configs.append(site_config.PROD_CONFIG)

    for config in configs:
        site.url = config.site_url
        gen_site(site, config)

if __name__ == "__main__":
    main()
