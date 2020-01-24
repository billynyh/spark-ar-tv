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
  'pl': 'Polish',
  'ro': 'Romanian',
  'hr': 'Croatian',
  'sk': 'Slovak',
  'el': 'Greek',
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

def get_lang_nav(site, langs):
    return [LangNavItem(lang, "%s/%s/index.html" % (site.url, lang)) for lang in langs]

def get_navs(master, site):
    languages = site.site_config.languages
    top_langs = ['global'] + [l for l in languages if master.lang_sites[l].num_videos > 100]
    secondary_langs = [l for l in languages if not l in top_langs]
    # language nav, topic nav
    navs = {
        'top_lang': get_lang_nav(site, top_langs),
        'secondary_lang': get_lang_nav(site, secondary_langs),
        'topic': get_topic_nav(master.global_site),
        'other': []
    }
    return navs
