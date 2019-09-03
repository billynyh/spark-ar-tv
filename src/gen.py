import argparse
import pprint
import json
import shutil
import os.path

import config_factory
import site_config
from lib import html_helper
from lib import util
from lib import yt_api_util
from lib.api import ApiDataLoader
from lib.data_loader import *
from lib.model import SiteConfig, PageConfig, Site

API_KEY = site_config.DEVELOPER_KEY

def open_out_file(out_dir, name):
    return open("%s/%s" % (out_dir, name), "w")

def week_pages(site, config):
    pages = []
    for week in site.groups_by_time:
        path = util.week_page_path(week)
        page_config = PageConfig()
        page_config.title = "%s | Spark AR TV" % week.title
        page_config.description = config.site_config.page_config.description
        if util.banner_generated(config.out_dir, week):
            page_config.og_image = util.get_group_banner_url(config, week)
        else:
            page_config.og_image = util.get_logo_url(config)

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

def topic_pages(site, config):
    if not site.topics:
        return []
    pages = []
    for topic in site.topics:
        path = util.topic_page_path(topic)
        page_config = PageConfig()
        page_config.title = "%s | Spark AR TV" % topic.title
        page_config.description = config.site_config.page_config.description
        if util.topic_banner_generated(config.out_dir, topic):
            page_config.og_image = util.get_topic_banner_url(config, topic)
        else:
            page_config.og_image = util.get_logo_url(config)

        pages.append((path, html_helper.gen_topic_html(site, page_config, topic)))

    page_config = PageConfig()
    page_config.title = "Topics | Spark AR TV"
    page_config.description = config.site_config.page_config.description
    pages.append(("topics/index.html", html_helper.gen_topic_list_html(site, page_config)))
    return pages

def facebook_pages(site, config):
    page_config = PageConfig()
    page_config.title = "Facebook | Spark AR TV"
    page_config.description = config.site_config.page_config.description
    return [("facebook.html", html_helper.gen_facebook_html(site, page_config))]

def gen_lang_site(site, config):
    lang = site.lang
    out_dir = "%s/%s" % (config.out_dir, lang)
    util.mkdir(out_dir)
    util.mkdir("%s/weeks" % out_dir)

    pages = standard_pages(site, config) + week_pages(site, config)

    if site.topics:
        util.mkdir("%s/topics" % out_dir)
        pages += topic_pages(site, config)
    if site.facebook:
        pages += facebook_pages(site, config)

    for page in pages:
        with open_out_file(out_dir, page[0]) as outfile:
            outfile.write(page[1])
            print("Generated %s" % outfile.name)

def gen_global_site(config):
    site = global_site(config, API_KEY)
    gen_lang_site(site, config)

def gen_site(config):
    for lang in config.site_config.languages:
        site = single_lang_site(config, lang, API_KEY)
        gen_lang_site(site, config)

    gen_global_site(config)

    # Copy assets
    util.copy_all_assets(config)


def main(prod=False):
    util.prepare_cache()

    config = config_factory.load(prod)
    gen_site(config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Site generation')
    parser.add_argument('--prod', action='store_true')
    args = parser.parse_args()
    main(prod=args.prod)
