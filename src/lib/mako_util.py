
def wrap(context, path):
    return "%s/%s" % (context.get('site').url, path)

def wrap_lang(context, path):
    site = context.get('site')
    return "%s/%s/%s" % (site.url, site.lang, path)

def asset(context, path):
    return wrap(context, "assets/%s" % path)

DISPLAY_NAME = {
  'en': 'English',
  'es': 'Spanish',
  'pt': 'Portuguese',
  'ru': 'Russian',
}

def all_languages(context):
    site_config = context.get('site').site_config
    return [(lang, DISPLAY_NAME[lang]) for lang in site_config.languages]
