
def wrap(context, path):
    return "%s/%s" % (context.get('site').url, path)

def wrap_lang(context, path):
    site = context.get('site')
    return "%s/%s/%s" % (site.url, site.lang, path)

def asset(context, path):
    return wrap(context, "assets/%s" % path)

def all_languages(context):
    site_config = context.get('site').site_config
    langs = site_config.languages + ['global']
    return [(lang, DISPLAY_NAME[lang]) for lang in langs]
