import argparse
import pprint
import json
import shutil
import os.path

import config_factory
import site_config
from lib.html_helper import HtmlHelper
from lib import json_helper
from lib import util
from lib import yt_api_util
from lib.api import ApiDataLoader
from lib.data_loader import *
from lib.model import SiteConfig, PageConfig, Site
from multiprocessing import Pool

html_helper = HtmlHelper()

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
    
    pages = [
        ("index.html", html_helper.gen_timeline_html(site, page_config)),
        ("full-list.html", html_helper.gen_timeline_html(site, page_config, full=True)),
        ("debug.html", html_helper.gen_debug_html(site, page_config)),
    ]
    pages.append(("channels.html", html_helper.gen_channel_html(site, page_config)))
    return pages

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
    return pages

def facebook_pages(site, config):
    page_config = PageConfig()
    page_config.title = "Facebook | Spark AR TV"
    page_config.description = config.site_config.page_config.description
    return [("facebook.html", html_helper.gen_facebook_html(site, page_config))]

def interviews_pages(site, config):
    page_config = PageConfig(config.site_config.page_config)
    page_config.title = "Interviews | Spark AR TV"
    if site.interviews:
        page_config.og_image = util.get_group_banner_url(config, site.interviews[0])
    return [("interviews.html", html_helper.gen_interviews_html(site, page_config))]

def custom_pages(site, config):
    pages = []
    for x in site.custom:
        page_config = PageConfig(config.site_config.page_config)
        page_config.title = "%s | Spark AR TV" % x['title']

        pages.append((
            "%s.html" % x['slug'], 
            html_helper.gen_fb_videos_html(site, page_config, x)
        ))
    return pages

def blogs(site, config):
    pages = []
    for x in site.blogs:
        page_config = PageConfig(config.site_config.page_config)
        page_config.title = "%s | Spark AR TV" % x['title']
        page_config.og_image = util.get_blog_banner_url(config, x['slug'])
        pages.append((
            "blogs/%s.html" % x['slug'], 
            html_helper.gen_blog_html(site, page_config, x)
        ))
    return pages

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
    if site.interviews:
        pages += interviews_pages(site, config)
    if site.custom:
        pages += custom_pages(site, config)
    if site.blogs:
        util.mkdir("%s/blogs" % out_dir)
        pages += blogs(site, config)

    for page in pages:
        with open_out_file(out_dir, page[0]) as outfile:
            outfile.write(page[1])
            print("Generated %s" % outfile.name)

def gen_global_json(site, config):
    pages = [
        ('nav.json', json_helper.nav_json(site))
    ]
    out_dir = "%s/global" % (config.out_dir)
    for page in pages:
        with open_out_file(out_dir, page[0]) as outfile:
            outfile.write(page[1])
            print("Generated %s" % outfile.name)

def gen_global_site(master):
    config = master.config
    site = master.global_site

    gen_lang_site(site, config)
    gen_global_json(site, config)

def gen_site(config):
    master = master_site(config)

    html_helper.master = master
    html_helper.config = config
    html_helper.global_site = master.global_site
  
    langs = [] # config.site_config.languages
    if config.use_multi_process:
        pool = Pool(5)
        pool.starmap(gen_lang_site, [(master.lang_sites[lang], config) for lang in langs])
    else:
        [gen_lang_site(master.lang_sites[lang], config) for lang in langs]
    gen_global_site(master)

    # Copy assets
    util.copy_all_assets(config)


def main(args):
    prod = args.prod
    assets_only = args.assets

    util.prepare_cache()

    config = config_factory.load(prod)
    if assets_only:
        util.copy_all_assets(config)
    else:
        gen_site(config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Site generation')
    parser.add_argument('--prod', action='store_true')
    parser.add_argument('--assets', action='store_true')
    args = parser.parse_args()
    main(args)
