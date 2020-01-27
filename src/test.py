import config_factory
import site_config
from lib import data_loader
from lib import util
from lib import sitemap_helper

from pprint import pprint

def test_extract_youtube_id():
    tests = [
        "IDI6xi9z3Zk",
        "/watch?v=IDI6xi9z3Zk",
        "/watch?v=IDI6xi9z3Zk //comment",
        "/watch?v=IDI6xi9z3Zk&t=1",
        "/watch?v=IDI6xi9z3Zk&t=1 //comment",
    ]
    for t in tests:
        print(util.extract_youtube_id(t))

if __name__ == "__main__":
    #test_extract_youtube_id()

    config = config_factory.load(False)
    master = data_loader.master_site(config)
    sitemap = sitemap_helper.load_sitemap(master, config)
    pprint(sitemap)
