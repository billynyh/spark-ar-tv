import site_config
from lib import data_loader
from lib import util

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
    test_extract_youtube_id()

    config = site_config.LOCAL_CONFIG
    site = data_loader.load_site_data(config)
    data_loader.group_by_time(site.video_data)
