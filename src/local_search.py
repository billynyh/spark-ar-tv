import argparse
import config_factory
import site_config
from lib.data_loader import *

def search(ids, video_data, keyword, debug, search_tags):
    has_result = False
    for id in ids:
        video = video_data[id]
        match = False
        if keyword in video.title.lower():
            match = True
            if debug:
                print("- title: %s" % video.title)
        if search_tags:
            for tag in video.metadata:
                if keyword in tag.lower():
                    match = True
                    if debug:
                        print("- tag: %s" % tag)
        if match:
            print("%s // %s | %s" % (video.id, video.title, video.published_at))
            has_result = True

def main(keyword, debug, search_tags = False):
    config = config_factory.load(False)
    master = master_site(config)
    video_data = master.global_site.video_data

    print("\nLocal search: %s" % keyword)
    for g in master.global_site.groups_by_week:
        #print("# %s" % g.title)
        search(g.ids, video_data, keyword, debug, search_tags)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Local search')
    parser.add_argument('keyword')
    parser.add_argument('--debug', default=False, action='store_true')
    parser.add_argument('--tags', default=False, action='store_true')
    args = parser.parse_args()
    main(args.keyword.lower(), debug = args.debug, search_tags = args.tags)
