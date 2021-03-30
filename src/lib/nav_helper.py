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
  'sk': 'Slovak',
  'el': 'Greek',
  'fa': 'Persian',
  'ko': 'Korean',
  'cs': 'Czech',
  'lt': 'Lithuanian',
  'hi': 'Hindi',
  'ne': 'Nepali',
  'ml': 'Malayalam',
  'vi': 'Vietnamese',
  'fil': 'Filipino',
  'te': 'Telugu',
  'ka': 'Georgian',
  'hu': 'Hungarian',
  'mn': 'Mongolian',
  'km': 'Khmer',
  'uz': 'Uzbek',
  'si': 'Sinhala',
  'az': 'Azerbaijani',
  'global': 'All Languages',
}

CHANNEL_LIST_DISPLAY_NAME = {
  'beginner': 'Channels for beginner',
  'featured': 'Featured channels',
}

def lang_display_name(lang):
    return LANG_DISPLAY_NAME[lang]

def get_lang_nav_item(site, lang):
    title = LANG_DISPLAY_NAME[lang]
    url = "%s/%s/index.html" % (site.url, lang)
    return {
        'title': title,
        'url' : url,
        'video_count': 0,
    }

def get_topic_nav_item(site, topic):
    title = topic.title
    url = util.topic_page_url(site, topic)
    video_count = len(topic.ids)
    return {
        'title': title,
        'url' : url,
        'video_count': video_count,
    }

def get_topic_nav(site):
    return [get_topic_nav_item(site, t)  for t in site.topics]

def get_lang_nav(site, langs):
    return [get_lang_nav_item(site, lang) for lang in langs]

def get_navs(master, site):
    languages = site.site_config.languages
    top_langs = ['global'] + [l for l in languages if master.lang_sites[l].num_videos > 100]
    secondary_langs = [l for l in languages if not l in top_langs]
    # language nav, topic nav
    navs = {
        'top_langs': get_lang_nav(site, top_langs),
        'secondary_langs': get_lang_nav(site, secondary_langs),
        'topics': get_topic_nav(master.global_site),
        'other': []
    }
    return navs

