from mako.template import Template
from mako.lookup import TemplateLookup

from lib import debug_util
from lib import util
from lib.nav_helper import get_navs

def large_thumb(ids):
    return len(ids) <= 12

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
            nav_json_url = "%s/global/nav.json" % site.url,
            debug = False, #True,
            **kwargs)

    def gen_debug_html(self, site, page):
        t = self.get_template('debug.html')
        return self.render(t, site=site, page = page)

    def gen_channels_html(self, site, page):
        t = self.get_template('channels.html')
        return self.render(t, site=site, page = page)

    def gen_facebook_html(self, site, page):
        t = self.get_template('facebook.html')
        return self.render(t, site=site, page = page, groups=site.facebook)

    def gen_music_html(self, site, page):
        t = self.get_template('facebook.html')
        return self.render(t, site=site, page = page, groups=site.music)

    def gen_interviews_html(self, site, page):
        t = self.get_template('facebook.html')
        return self.render(t, site=site, page = page, groups=site.interviews)

    def gen_timeline_html(self, site, page, full = False):
        t = self.get_template('index.html')
        return self.render(t, 
            site = site, 
            page = page, 
            link_to_group = True,
            full = full)

    def gen_week_html(self, site, page, week):
        t = self.get_template('week.html')
        return self.render(t, 
            site = site,
            page = page,
            week = week, 
            large_thumb = large_thumb(week.ids))
     
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
            large_thumb = large_thumb(topic.ids))

    def gen_single_channel_html(self, site, page, group):
        t = self.get_template('single_channel.html')
        return self.render(t, 
            site = site,
            page = page,
            group = group,
            large_thumb = large_thumb(group.ids),
            use_yt_channel_url = True,
            )

    def gen_fb_videos_html(self, site, page, param):
        t = self.get_template('fb_videos.html')
        return self.render(t,
            site = site,
            fb_video_urls = param['urls'],
            fb_app_id = '481172182744207',
            page = page,
            title = param['title'],
            )
    
    def gen_blog_html(self, site, page, param):
        t = self.get_template('blog.html')
        html = open('data/blogs/%s.html' % param['slug']).read()
        return self.render(t,
            site = site,
            page = page,
            title = param['title'],
            content = html,
            )

    def gen_sitemap_html(self, site, page, sitemap):
        t = self.get_template('sitemap.html')
        return self.render(t,
            site = site,
            page = page,
            sitemap = sitemap,
            )
