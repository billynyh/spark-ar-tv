from lib.model import GeneratorConfig

DEVELOPER_KEY = "AIzaSyDqKnN-e5o1z9zj6RMbDfxef9VuFSpLB84"
CACHE_DIR = "_cache"

# site
PROD_CONFIG = GeneratorConfig(
    site_url = "https://billynyh.github.io/spark-ar-tv",
    out_dir = ".."
)

LOCAL_CONFIG = GeneratorConfig(
    site_url = "http://localhost:8000",
    out_dir = "_out"
)

# playlist
PLAYLIST_CHANNEL = "UCDEJIEZnODawQRONeYbKbMA"
PLAYLIST_ID = "PLJ-lx8QFIxZZ-sj9f_4KAD5KIT3GdcMo1"