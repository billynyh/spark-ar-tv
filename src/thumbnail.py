import urllib.request
import shutil

import site_config
from lib import data_loader, util
from lib.data_loader import global_site, parse
from lib import image_helper

def download_all(video_data):
    caches = util.get_cache_images()
    need_fetch = [id for id in video_data.keys() if not id in caches]
    for id in need_fetch:
        url = video_data[id].thumbnail_url
        with urllib.request.urlopen(url) as response:
            with open(util.get_cache_image_path(id), "wb") as outfile:
                shutil.copyfileobj(response, outfile)
                print("Downloaded %s" % outfile.name)

def generate_week_thumbnails(site):
    for g in site.groups_by_time:
        img = image_helper.group_thumbnail_collage(site, g.ids)
        outfile = util.get_group_banner_path(config.out_dir, g)
        img.save(outfile, "JPEG")
        print("Saved %s" % outfile)

def generate_topics_thumbnails(site):
    groups = parse("data/topic-thumbnails.txt")
    for g in groups:
        img = image_helper.group_thumbnail_collage(site, g.ids)
        outfile = util.get_topic_banner_path(config.out_dir, g)
        img.save(outfile, "JPEG")
        print("Saved %s" % outfile)
        

if __name__ == "__main__":
    config = site_config.generator

    site = global_site(config, site_config.DEVELOPER_KEY)
    download_all(site.video_data)
    generate_topics_thumbnails(site)
    # generate_week_thumbnails(site)
