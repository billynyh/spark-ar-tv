from mako.template import Template
from mako.lookup import TemplateLookup

from lib import debug_util
from lib import util

def get_template(filename):
    lookup = TemplateLookup(directories=['.'])
    t = Template(filename="layouts/%s" % filename, lookup=lookup)
    return t

def gen_debug_html(site, page):
    debug_text = debug_util.get_message(site)
    t = get_template('debug.html')
    return t.render(site=site, page = page, debug_text=debug_text)

def gen_channel_html(site, page):
    t = get_template('channels.html')
    return t.render(site=site, page = page)

def gen_timeline_html(site, page):
    t = get_template('index.html')
    return t.render(site = site, page = page, link_to_group = True)

def gen_week_html(site, page, week):
    t = get_template('week.html')
    return t.render(
        site = site,
        page = page,
        week = week, 
        large_thumb= True)
    
def gen_topic_html(site, page, topic):
    t = get_template('topic.html')
    return t.render(
        site = site,
        page = page,
        topic = topic, 
        large_thumb = True)
    
