from lib import util

LANG_DISPLAY_NAME = {
  'en': 'English',
  'es': 'Spanish',
  'pt': 'Portuguese',
  'ru': 'Russian',
  'id': 'Indonesian',
  'it': 'Italian',
  'jp': 'Japanese',
  'nl': 'Dutch',
  'global': 'All Languages',
}

class TopicNavItem:
    def __init__(self, topic, url):
        self.show_video_count = True
        self.title = topic.title
        self.video_count = len(topic.ids)
        self.url = url

class LangNavItem:
    def __init__(self, lang, url):
        self.show_video_count = False
        self.title = LANG_DISPLAY_NAME[lang]
        self.url = url

def get_topic_nav(site):
    return [TopicNavItem(t, util.topic_page_url(site, t)) for t in site.topics]

def get_lang_nav(site):
    languages = ['global'] + site.site_config.languages
    return [LangNavItem(lang, "%s/%s/index.html" % (site.url, lang)) for lang in languages]

def get_navs(master, site):
    # language nav, topic nav
    navs = {
        'lang': get_lang_nav(site),
        'topic': get_topic_nav(master.global_site),
        'other': []
    }
    return navs
    