import json
from lib.nav_helper import get_topic_nav

def nav_json(site):
    topics = [{'url': t.url, 'video_count':t.video_count} for t in get_topic_nav(site)]
    obj = {
        'topics': topics,
    }
    return json.dumps(obj)
