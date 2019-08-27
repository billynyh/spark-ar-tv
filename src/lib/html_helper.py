from mako.template import Template
from mako.lookup import TemplateLookup

from lib import debug_util

def get_template(filename):
    lookup = TemplateLookup(directories=['.'])
    t = Template(filename="layouts/%s" % filename, lookup=lookup)
    return t

def gen_debug_html(site):
    debug_text = debug_util.get_message(site)
    t = get_template('debug.html')
    return t.render(site=site, debug_text=debug_text)

def gen_channel_html(site):
    t = get_template('channels.html')
    return t.render(site=site)

def gen_timeline_html(site):
    t = get_template('index.html')
    return t.render(site = site)
