import pprint
import json
import shutil
import os.path

import config
from lib import html_helper
from lib import util
from lib import yt_api_util
from lib.api import ApiDataLoader
from lib.data_loader import load_site_config
from lib.model import SiteConfig
from lib.const import *


def open_out_file(name):
    return open("%s/%s" % (config.OUT_DIR, name), "w")

def main():
    site = load_site_config(config.DEVELOPER_KEY)

    html = html_helper.gen_html(site)
    with open_out_file("index.html") as outfile:
        outfile.write(html)
        print("Generated %s" % outfile.name)
    with open_out_file("debug.html") as outfile:
        outfile.write(html)
        print("Generated %s" % outfile.name)
    util.copy_all("assets", config.OUT_ASSETS_DIR)
    
if __name__ == "__main__":
    main()
