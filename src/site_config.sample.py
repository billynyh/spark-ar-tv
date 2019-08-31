from lib.model import GeneratorConfig

DEVELOPER_KEY = "" 
CACHE_DIR = "_cache"

# site
PROD_CONFIG = GeneratorConfig(
    site_url = "https://billynyh.github.io/spark-ar-tv",
    site_title = "Spark AR TV",
    site_description = "Unofficial Spark AR video tutorial collections",
    out_dir = "..",
    data_dir = "data/en"
)

LOCAL_CONFIG = GeneratorConfig(
    site_url = "http://localhost:8000",
    site_title = "Spark AR TV",
    site_description = "Unofficial Spark AR video tutorial collections",
    out_dir = "_out",
    data_dir = "data/en"
)

# playlist
PLAYLIST_CHANNEL = ""
PLAYLIST_ID = ""
