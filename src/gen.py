import argparse
import pprint
import json
import shutil
import os.path

import site_config
from lib import html_helper
from lib import util
from lib import yt_api_util
from lib.api import ApiDataLoader
from lib.data_loader import *
from lib.model import SiteConfig, PageConfig, Site

def open_out_file(out_dir, name):
    return open("%s/%s" % (out_dir, name), "w")

def week_pages(site, config):
    pages = []
    for week in site.groups_by_time:
        path = util.week_page_path(week)
        page_config = PageConfig()
        page_config.title = "%s | Spark AR TV" % week.title,
        page_config.description = config.site_config.page_config.description,
        page_config.og_image = util.get_group_banner_url(config, week)

        pages.append((path, html_helper.gen_week_html(site, page_config, week)))
    return pages

def standard_pages(site, config):
    page_config = PageConfig(config.site_config.page_config)
    page_config.og_image = util.get_logo_url(config)
    
    return [
        ("index.html", html_helper.gen_timeline_html(site, page_config)),
        ("debug.html", html_helper.gen_debug_html(site, page_config)),
        ("channels.html", html_helper.gen_channel_html(site, page_config)),
    ]

def single_lang_site(config, lang):
    site = load_site_data(
        config, 
        path = "data/%s" % lang,
        api_key = site_config.DEVELOPER_KEY)
    site.url = config.site_config.url
    site.site_config = config.site_config
    site.lang = lang
    return site

def gen_lang_site(site, config):
    lang = site.lang
    pages = standard_pages(site, config) + week_pages(site, config)

    out_dir = "%s/%s" % (config.out_dir, lang)
    util.mkdir(out_dir)
    util.mkdir("%s/weeks" % out_dir)

    for page in pages:
        with open_out_file(out_dir, page[0]) as outfile:
            outfile.write(page[1])
            print("Generated %s" % outfile.name)

def gen_global_site(config):
    site = Site()
    site.video_data = None
    site.url = config.site_config.url
    site.site_config = config.site_config
    site.lang = "global"
    site.groups = load_global_groups(config)

    all_youtube_ids = [id for g in site.groups for id in g.ids]
    site.video_data = load_video_data(all_youtube_ids, site_config.DEVELOPER_KEY)
    site.groups_by_time = group_by_time(site.video_data)

    gen_lang_site(site, config)

def gen_site(config):
    for lang in config.site_config.languages:
        site = single_lang_site(config, lang)
        gen_lang_site(site, config)

    gen_global_site(config)

    # Copy assets
    util.copy_all_assets(config)


def main(prod=False):
    util.prepare_cache()

    config = site_config.generator
    gen_site(config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Site generation')
    parser.add_argument('--prod', action='store_true')
    args = parser.parse_args()
    main(prod=args.prod)
