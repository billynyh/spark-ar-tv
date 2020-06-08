import urllib.request
import shutil
import random
import config_factory
import site_config
from lib import data_loader, util
from lib.data_loader import global_site, parse, master_site
from lib import image_helper

def ping_all(video_data):
    caches = util.get_cache_images()
    need_fetch = [id for id in video_data.keys() if not id in caches]
    cnt = 0
    total = len(need_fetch)
    print()
    for id in need_fetch:
        print("\r%d/%d" % (cnt, total), end="\r")
        url = video_data[id].thumbnail_url
        cnt += 1
        try:
            r = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            print(id)

def download_all(video_data):
    caches = util.get_cache_images()
    need_fetch = [id for id in video_data.keys() if not id in caches]
    for id in need_fetch:
        url = video_data[id].thumbnail_url
        with urllib.request.urlopen(url) as response:
            with open(util.get_cache_image_path(id), "wb") as outfile:
                shutil.copyfileobj(response, outfile)
                print("Downloaded %s" % outfile.name)

def generate_day_thumbnail(site, g):
    ids = list(g.ids)
    random.shuffle(ids)
    ids = ids[:4]
    video_data = {id:site.video_data[id] for id in ids}
    download_all(video_data)

    img = image_helper.group_thumbnail_collage(site, ids)
    outfile = util.get_group_banner_path(config.out_dir, g)
    img.save(outfile, "JPEG")
    print("Saved %s" % outfile)

def generate_week_thumbnails(site):
    for g in site.groups_by_week:
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
    groups = parse("data/thumbnails-topics.txt")
    for g in groups:
        video_data = {id:site.video_data[id] for id in g.ids}
        download_all(video_data)
        img = image_helper.group_thumbnail_collage(site, g.ids)
        outfile = util.get_topic_banner_path(config.out_dir, g)
        print(outfile)
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

def generate_channel_thumbnails(site):
    channel_ids = "UCh2gFKv1dmrTxmMRgzchmrQ UC3zmATtNhDuYOketH1zF5sw UCfgGh_akZMp7t_ln7t5OnPQ UC2Cixv8Y6__g2tO8_AlJD0A UC4-1nuI6rLNfCGf3Zzh4RYA UCZMGG9QLteZtdEkEoRjeE1w UC5K-VEQJLcBJZqjzp7LFowQ UCw-3EcRVMdqQehzfR5JKVzQ UCKqZArZmJK3jbqUj2Dth3uA UCI2CajpqcsjV8iGgUoljDJw UCYTyihvxy6KEcQrzXzp5j-w UCgluiH_ayEPx4mor_08nkGw UCWkSJvFF7m-CstbIh9YnKYw UCjwbuWu-ORxglkjo6NoS-7g UCcFy_yfaBHp2z-fceORWsWg UCIklWn98ibY3l6cPtNN4c5Q UCtTBLIjp8tpto5R9JYM8BNg UCXzGwiho8xLhl11uGAhuNuA UC4-phUrGgm63fZ9qZ1GOxBQ UCDWHU8_AeK4ZcgCnrN7lUUQ UCNObtXN2IyZCCppgcq1yapA UCO6QRYjZfbYcdwwHv5vmf3Q UCI7pSUi_CX5ElJGfOl6n4cA UCMCwClnJbWBiu_hbDKhVPlQ UCcx9UsvNp6HVsbQ7PJilk1w UCAHV1Y1ufvxC_cclL0GjOCw UC_ycBf44SNpOc7w6kvYkufA UCtoRX-yMVpmlJFmo8i9aZyQ".split(" ")
    for g in site.groups:
        cid = site.video_data[g.ids[0]].channel_id
        if (cid in channel_ids):
            ids = sorted(g.ids, key = lambda id: -int(site.video_data[id].view_count))[:4]
            print(ids)
            video_data = {id:site.video_data[id] for id in ids}
            download_all(video_data)
            img = image_helper.group_thumbnail_collage(site, ids)
            outfile = util.get_channel_banner_path(config.out_dir, cid)
            img.save(outfile, "JPEG")
            print("Saved %s" % outfile)
    
def main_topics():
    master = master_site(config)
    site = master.global_site
    generate_topics_thumbnails(site)
    return

    #generate_channel_thumbnails(site)

def main():
    master = master_site(config)
    site = master.global_site
    ids = 'OzvXhri662A Cd253TiCisw D5yo6Kq_hi4 oxjJQjYg1gc'
    ids = ids.split()

    video_data = {id:site.video_data[id] for id in ids}
    download_all(video_data)

    generate_custom_week_thumbnails(site, ids, 'week-2020-06-01')
    #generate_channel_thumbnails(site)

def main_ping():
    master = master_site(config)
    site = master.global_site
    ping_all(site.video_data)

def main_day():
    master = master_site(config)
    site = master.global_site

    groups = site.groups_by_day[0:2]
    for g in groups:
        generate_day_thumbnail(site, g)
    


if __name__ == "__main__":
    config = config_factory.load()
    #main_ping()
    #main_topics()
    
    main()
    #main_day()
