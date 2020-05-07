import json
from lib.nav_helper import get_topic_nav
from lib.nav_helper import get_navs
from lib import util
from lib import data_loader

def get_recent_weeks(master, site):
    weeks = site.groups_by_week[:6]
    return [week_to_dict(w, site) for w in weeks]

def get_featured_contents(master, site):
    channels = site.groups_by_num_videos[:8]
    vids = site.most_viewed[:40]

    contents = []
    contents += [channel_to_dict(c, site) for c in channels]
    contents += [vid_to_content_dict(id, site) for id in vids]
    return contents

def nav_json(master, indent = None):
    site = master.global_site
    nav = get_navs(master, site)
    featured_contents = get_featured_contents(master, site)
    recent_weeks = get_recent_weeks(master, site)
    obj = {
      'nav': nav,
      'featured_contents': featured_contents,
      'recent_weeks': recent_weeks,
    }
    return json.dumps(obj, indent = indent)

def search_json(master):
    site = master.global_site
    vids = [vid_to_dict(v) for v in site.video_data.values()]
    vids = sorted(vids, key = lambda v: v['id'])

    return json.dumps(vids)

def week_to_dict(w, site):
    ids = data_loader.sort_by_view_count(w.ids, site.video_data)
    v = site.video_data[ids[0]]
    return {
        'url': util.week_page_url(site, 'global', w),
        'thumbnail_url': v.thumbnail_url,
        'title': w.title,
        'meta1': "Num videos: %d" % len(w.ids),
        'meta2': None,
    }

def channel_to_dict(c, site):
    ids = data_loader.sort_by_view_count(c.ids, site.video_data)
    v = site.video_data[ids[0]]
    channel_id = v.channel_id
    return {
        'url': util.channel_page_url(site, channel_id),
        'thumbnail_url': v.thumbnail_url,
        'title': "Channel: %s" % c.title,
        'meta1': "Num videos: %d" % len(c.ids),
        'meta2': None,
    }

def vid_to_content_dict(id, site):
    v = site.video_data[id]
    return {
        'url': v.video_url,
        'thumbnail_url': v.thumbnail_url,
        'title': "%s" % v.title,
        'meta1': v.channel_title,
        'meta2': "%s" % v.published_at,
    }

def vid_to_dict(v):
    return {
        'channel_title': v.channel_title,
        'channel_url': v.channel_url,
        'duration': v.duration,
        'id': v.id,
        'metadata': v.metadata,
        'published_at': v.published_at.strftime('%Y-%m-%d'),
        'thumbnail_url': v.highres_thumbnail_url,
        'title': v.title,
        'video_url': v.video_url,
    }
