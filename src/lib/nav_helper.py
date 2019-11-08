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
  'tr': 'Turkish',
  'fr': 'French',
  'de': 'German',
  'zh': 'Chinese',
  'iw': 'Hebrew',
  'ar': 'Arabic',
  'th': 'Thai',
  'global': 'All Languages',
}

CHANNEL_LIST_DISPLAY_NAME = {
  'beginner': 'Channels for beginner',
  'featured': 'Featured channels',
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

class NavItem:
    def __init__(self, title, url):
        self.show_video_count = False
        self.title = title
        self.url = url

def get_topic_nav(site):
    return [TopicNavItem(t, util.topic_page_url(site, t)) for t in site.topics]

def get_lang_nav(site):
    languages = ['global'] + site.site_config.languages
    return [LangNavItem(lang, "%s/%s/index.html" % (site.url, lang)) for lang in languages]

def get_channel_list_nav(site):
    channel_lists = site.channel_lists or []
    music = site.music or []
    interviews = site.interviews or []
    return [NavItem(l.title, "%s/global/%s.html" % (site.url, l.slug)) for l in channel_lists]\
      + [NavItem(l.title, "%s/global/%s.html" % (site.url, l.slug)) for l in music]\
      + [NavItem(l.title, "%s/global/%s.html" % (site.url, l.slug)) for l in interviews]

def get_navs(master, site):
    # language nav, topic nav
    navs = {
        'lang': get_lang_nav(site),
        'channel_list': get_channel_list_nav(master.global_site),
        'topic': get_topic_nav(master.global_site),
        'other': []
    }
    return navs
    
