import json
import re
import os
import shutil

from site_config import CACHE_DIR

def extract_youtube_id(s):
    s = re.sub(' //.*$', '', s)
    a = s.split("v=")
    if len(a) == 1:
        return s
    return a[1].split("&")[0]

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def prepare_cache():
    caches = [
        CACHE_DIR, 
        "%s/json" % CACHE_DIR, 
        "%s/images" % CACHE_DIR
    ]
    for c in caches:
        if not os.path.exists(c):
            os.mkdir(c)

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def get_cache_json_files():
    files = os.listdir("%s/json" % CACHE_DIR)
    return files

def get_cache_json_path(id):
    return "%s/json/%s" % (CACHE_DIR, id)

def get_cache_images():
    return os.listdir("%s/images" % CACHE_DIR)

def get_cache_image_path(id): 
    return "%s/images/%s" % (CACHE_DIR, id)

def delete_cache_json(id):
    p = get_cache_json_path(id)
    if os.path.exists(p):
        os.remove(p)
        return True
    return False

# copy all files inside src to dst, non recursive
def copy_all(src, dst):
    mkdir(dst)
    for f in os.listdir(src):
        shutil.copy("%s/%s" % (src, f), "%s/%s" % (dst, f))

def copy_all_assets(config):
    copy_all("assets", "%s/assets" % config.out_dir)

def dump_video_list(ids, video_data):
    return ["%s // %s" % (id, video_data[id].title) for id in ids]

def banner_generated(out_dir, g):
    path = get_group_banner_path(out_dir, g)
    return os.path.exists(path)

def get_group_banner_path(out_dir, g):
    slug = maybe_override(g.slug)
    return "%s/assets/banner/%s.jpg" % (out_dir, slug)

def get_group_banner_url(config, g):
    slug = maybe_override(g.slug)
    return "%s/assets/banner/%s.jpg" % (config.site_config.url, slug)

def get_topic_banner_path(out_dir, g):
    return "%s/assets/banner/topic-%s.jpg" % (out_dir, g.slug)

def get_topic_banner_url(config, g):
    return "%s/assets/banner/topic-%s.jpg" % (config.site_config.url, g.slug)

def get_blog_banner_path(out_dir, slug):
    return "%s/assets/banner/blog-%s.jpg" % (out_dir, slug)

def get_blog_banner_url(config, slug):
    return "%s/assets/banner/blog-%s.jpg" % (config.site_config.url, slug)

def topic_banner_generated(out_dir, g):
    path = get_topic_banner_path(out_dir, g)
    return os.path.exists(path)

def channel_banner_generated(out_dir, id):
    path = get_channel_banner_path(out_dir, id)
    return os.path.exists(path)

def get_channel_banner_path(out_dir, slug):
    return "%s/assets/banner/channel-%s.jpg" % (out_dir, slug)

def get_channel_banner_url(config, slug):
    return "%s/assets/banner/channel-%s.jpg" % (config.site_config.url, slug)

def get_logo_url(config):
    return "%s/assets/logo2.png" % (config.site_config.url)

def day_page_path(day):
    return "days/%s.html" % day.slug

def week_page_path(week):
    return "weeks/%s.html" % week.slug

def week_page_url(site, lang, week):
    return "%s/%s/%s" % (site.url, lang, week_page_path(week))

def topic_page_path(topic):
    return "topics/%s.html" % topic.slug

def topic_page_url(site, topic):
    return "%s/global/%s" % (site.url, topic_page_path(topic))

def channel_page_url(site, channel_id):
    return "%s/global/channels/%s.html" % (site.url, channel_id)

def maybe_override(slug):
    if slug == 'week-2020-07-13':
        return 'week-2020-07-13b'
    return slug
