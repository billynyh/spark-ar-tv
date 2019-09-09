from mako.template import Template
from mako.lookup import TemplateLookup

from lib import debug_util
from lib import util
from lib.nav_helper import get_navs

class HtmlHelper:

    master = None
    config = None
    global_site = None

    def get_template(self, filename):
        lookup = TemplateLookup(directories=['.'])
        t = Template(filename="layouts/%s" % filename, lookup=lookup)
        return t

    def render(self, t, site, **kwargs):
        return t.render(
            master = self.master,
            site = site,
            navs = get_navs(self.master, site),
            **kwargs)

    def gen_debug_html(self, site, page):
        debug_text = debug_util.get_message(site)
        t = self.get_template('debug.html')
        return self.render(t, site=site, page = page, debug_text=debug_text)

    def gen_channel_html(self, site, page):
        t = self.get_template('channels.html')
        return self.render(t, site=site, page = page)

    def gen_facebook_html(self, site, page):
        t = self.get_template('facebook.html')
        return self.render(t, site=site, page = page)

    def gen_timeline_html(self, site, page):
        t = self.get_template('index.html')
        return self.render(t, 
            site = site, 
            page = page, 
            link_to_group = True)

    def gen_week_html(self, site, page, week):
        t = self.get_template('week.html')
        return self.render(t, 
            site = site,
            page = page,
            week = week, 
            large_thumb= True)
     
    def gen_topic_list_html(self, site, page):
        t = self.get_template('topics.html')
        return self.render(t, 
            site = site,
            page = page,
            large_thumb = True)
        
    def gen_topic_html(self, site, page, topic):
        t = self.get_template('topic.html')
        return self.render(t, 
            site = site,
            page = page,
            topic = topic,
            large_thumb = True)

