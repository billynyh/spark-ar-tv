from mako.template import Template
from mako.lookup import TemplateLookup

from lib.const import *
from lib.model import Group
from lib import data_loader
from lib import util

def get_template(filename):
    lookup = TemplateLookup(directories=['.'])
    t = Template(filename="layouts/%s" % filename, lookup=lookup)
    return t

def gen_debug_html(site):
    video_data = site.video_data
    (most_viewed, latest) = data_loader.sort_videos(video_data)

    NUM = 18
    debug_groups = [
      Group("Latest", latest[:NUM]),
      Group("Most Viewed", most_viewed[:NUM]),
    ]

    dump_video_list = ["# Latest"]
    dump_video_list += util.dump_video_list(latest[:NUM], video_data)
    dump_video_list += ["", "# Most viewed"]
    dump_video_list += util.dump_video_list(most_viewed[:NUM], video_data)

    debug_text = '\n'.join(dump_video_list)

    t = get_template('debug.html')
    return t.render(site=site, debug_text=debug_text)

def gen_channel_html(site):
    t = get_template('channels.html')
    return t.render(site=site)

def gen_timeline_html(site):

    t = get_template('index.html')
    return t.render(site = site)

