from lib import nav_helper
from lib import util

def load_sitemap(master, config):
    sections = []
    site = master.global_site

    sections += [
        global_section(site, config),
        global_topic_section(site, config),
        global_week_section(site, config),
    ]

    languages = site.site_config.languages
    for lang in languages:
        sections += [
            single_lang_section(master.lang_sites[lang], config, lang),
            single_lang_week_section(master.lang_sites[lang], config, lang),
        ]

    return sections

def global_section(site, config):
    title = "All languages"
    links = standard_lang_site_pages(site, config, 'global') + [
        ('Spark AR official videos', "%s/global/facebook.html" % (site.url)),
    ]
    return (title, links)

def global_topic_section(site, config):
    title = "Topics"
    links = [(g.title, util.topic_page_url(site, g)) for g in site.topics]
    return (title, links)

def global_week_section(site, config):
    title = "Weekly collections"
    links = [(g.title, util.week_page_url(site, 'global', g)) for g in site.groups_by_week]
    return (title, links)

def single_lang_section(site, config, lang):
    title = nav_helper.lang_display_name(lang)
    links = standard_lang_site_pages(site, config, lang)
    return (title, links)

def single_lang_week_section(site, config, lang):
    title = "%s weekly collections" % nav_helper.lang_display_name(lang)
    title = None
    links = [(g.title, util.week_page_url(site, lang, g)) for g in site.groups_by_week]
    return (title, links)

def standard_lang_site_pages(site, config, lang):
    return [
        ('Recent videos', "%s/%s/index.html" % (site.url, lang)),
        ('All videos', "%s/%s/full-list.html" % (site.url, lang)),
        ('Channels', "%s/%s/channels.html" % (site.url, lang)),
    ]
