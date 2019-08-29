import urllib.request
import shutil

import config
from lib import data_loader, util
from lib.data_loader import load_site_config
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


if __name__ == "__main__":
    site = data_loader.load_site_config()
    download_all(site.video_data)
    site = load_site_config(config.DEVELOPER_KEY)
    for g in site.groups_by_time:
        img = image_helper.group_thumbnail_collage(site, g.ids)
        outfile = util.get_group_banner_path(g)
        img.save(outfile, "JPEG")
        print("Saved %s" % outfile)
