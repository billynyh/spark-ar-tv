
class GeneratorConfig:
    def __init__(self, site_url, site_title, site_description, out_dir):
        self.site_url = site_url
        self.out_dir = out_dir
        self.out_assets_dir = "%s/assets" % out_dir
        self.site_title = site_title
        self.site_description = site_description

class SiteConfig:
    video_data = None
    groups = None
    groups_by_time = None
    most_viewed = None
    latest = None
    url = None

class PageConfig:
    def __init__(self, title, description, og_image):
        self.title = title
        self.description = description
        self.og_image = og_image

class Group:
    title = None
    slug = None
    ids = None

    def __init__(self, title, ids):
        self.title = title
        self.ids = ids
        self.slug = title.lower().replace(" ", "-")

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
        
