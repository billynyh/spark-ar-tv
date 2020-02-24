import json
from lib.nav_helper import get_topic_nav
from lib.nav_helper import get_navs

def nav_json(master):
    site = master.global_site
    navs = get_navs(master, site)

    return json.dumps(navs)

def search_json(master):
    site = master.global_site
    vids = [vid_to_dict(v) for v in site.video_data.values()]

    return json.dumps(vids)


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
