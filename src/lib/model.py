import re
# Config object

class GeneratorConfig2:
    def __init__(self, site_url, site_title, site_description, out_dir, data_dir):
        self.site_url = site_url
        self.out_dir = out_dir
        self.out_assets_dir = "%s/assets" % out_dir
        self.site_title = site_title
        self.site_description = site_description
        self.data_dir = data_dir

class GeneratorConfig:
    out_dir = None
    cache_dir = None

class SiteConfig:
    url = None
    page_config = None
    languages = []
    enable_ga = False

class PageConfig:
    title = None
    description = None
    og_image = None

    def __init__(self, src=None):
        if src:
            self.title = src.title
            self.description = src.description
            self.og_image = src.og_image

# Model
class Site:
    video_data = None
    url = None
    lang = None
    site_config = None
    groups = []
    groups_by_time = []
    most_viewed = []
    latest = []
    topics = []

class Group:
    title = None
    slug = None
    ids = None

    def __init__(self, title, ids):
        self.title = title
        self.ids = ids
        slug = title.lower()
        for c in "/!@#$%^&*()":
            slug = slug.replace(c, "")
        self.slug = re.sub(r" +", "-", slug)

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
        
