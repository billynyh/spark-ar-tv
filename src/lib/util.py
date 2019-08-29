import json
import re
import os
import shutil

import config
from lib.const import *

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
        config.CACHE_DIR, 
        "%s/json" % config.CACHE_DIR, 
        "%s/images" % config.CACHE_DIR
    ]
    for c in caches:
        if not os.path.exists(c):
            os.mkdir(c)

def get_cache_json_files():
    files = os.listdir("%s/json" % config.CACHE_DIR)
    return files

def get_cache_json_path(id):
    return "%s/json/%s" % (config.CACHE_DIR, id)

def get_cache_images():
    return os.listdir("%s/images" % config.CACHE_DIR)

def get_cache_image_path(id): 
    return "%s/images/%s" % (config.CACHE_DIR, id)

# copy all files inside src to dst, non recursive
def copy_all(src, dst):
    for f in os.listdir(src):
        shutil.copy("%s/%s" % (src, f), "%s/%s" % (dst, f))

def dump_video_list(ids, video_data):
    return ["%s // %s" % (id, video_data[id].title) for id in ids]

def get_group_banner_path(g):
    return "%s/assets/banner/%s.jpg" % (config.OUT_DIR, g.slug)
    
