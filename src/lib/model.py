

class SiteConfig:
    video_data = None
    groups = None
    groups_by_time = None
    most_viewed = None
    latest = None

class Group:
    title = None
    ids = None

    def __init__(self, title = None, ids = None):
        self.title = title
        self.ids = ids

class Video:
    id = None
    title = None
    thumbnail_url = None
    highres_thumbnail_url = None
    channel_id = None
    channel_title = None
    channel_url = None
    duration = None
    view_count = None
    published_at = None
    video_url = None
        
