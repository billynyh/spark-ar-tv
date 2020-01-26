import json
from lib.nav_helper import get_topic_nav
from lib.nav_helper import get_navs

def nav_json(master):
    site = master.global_site
    navs = get_navs(master, site)

    return json.dumps(navs)
