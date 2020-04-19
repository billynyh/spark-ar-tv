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

def test_regroup():
    config = config_factory.load(False)
    master = data_loader.master_site(config, merge_small_groups = False)

    import cleanup
    site = master.lang_sites['ru']
    print(len(site.groups))

    print("---")
    new_groups = cleanup.regroup_by_channel(site.groups, site.video_data)
    new_groups = sorted(new_groups, key = lambda group: group.title.lower()) 
    print(len(new_groups))

if __name__ == "__main__":
    #test_extract_youtube_id()
    test_regroup()
