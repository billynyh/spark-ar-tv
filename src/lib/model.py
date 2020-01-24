import re
# Config object

class GeneratorConfig:
    out_dir = None
    cache_dir = None
    site_config = None
    api_key = None
    global_only = False
    channel = True

class SiteConfig:
    url = None
    page_config = None
    languages = None
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
class MasterSite:
    lang_sites = {}
    global_site = None
    config = None

class Site:
    video_data = None
    url = None
    lang = None
    site_config = None
    groups = None
    groups_by_time = None
    most_viewed = None
    latest = None
    topics = None
    facebook = None
    interviews = None
    custom = None
    blogs = None
    gen_channel_html = False
    num_videos = 0

class Group:
    title = None
    slug = None
    ids = None

    def __init__(self, title, ids):
        self.title = title
        self.ids = ids
        self.slug = to_slug(title)

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
    raw_published_at = None
    video_url = None
    metadata = None
    live_broadcast_content = None

class ChannelList:
    slug = None
    title = None
    ids = None

    def __init__(self, slug):
        self.slug = to_slug(slug)
        self.ids = []

SLUG_OVERRIDE = {
    "native-ui-picker-slider": "native-ui",
    "random-image-game-head-quiz": "random-image-game",
}

def to_slug(s):
    slug = s.lower()
    for c in "/!@#$%^&*()":
        slug = slug.replace(c, "")
    slug = re.sub(r" +", "-", slug)
    slug = SLUG_OVERRIDE.get(slug, slug)
    return slug
