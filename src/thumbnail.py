import urllib.request
import shutil

import config_factory
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

def generate_custom_week_thumbnails(site, ids, group_slug):
    img = image_helper.group_thumbnail_collage(site, ids)
    outfile = "%s/assets/banner/%s.jpg" % (config.out_dir, group_slug)
    img.save(outfile, "JPEG")
    print("Saved %s" % outfile)

def generate_topics_thumbnails(site):
    groups = parse("data/topic-thumbnails.txt")
    for g in groups:
        img = image_helper.group_thumbnail_collage(site, g.ids)
        outfile = util.get_topic_banner_path(config.out_dir, g)
        img.save(outfile, "JPEG")
        print("Saved %s" % outfile)
        
def generate_facebook_thumbnails(site):
    video_data = {id:site.video_data[id] for g in site.facebook for id in g.ids}
    download_all(video_data)
    return
    for g in groups:
        img = image_helper.group_thumbnail_collage(site, g.ids)
        outfile = util.get_topic_banner_path(config.out_dir, g)
        img.save(outfile, "JPEG")
        print("Saved %s" % outfile)

if __name__ == "__main__":
    config = config_factory.load()

    site = global_site(config)
    #download_all(site.video_data)
    #generate_topics_thumbnails(site)
    # generate_week_thumbnails(site)
    #generate_facebook_thumbnails(site)
    ids = 'GUNl32dzslc,4g4CoL_KCkE,cWXuxhD7sAc,4BEKaaHmjfk'.split(',')
    generate_custom_week_thumbnails(site, ids, 'week-2019-09-16')
