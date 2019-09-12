import argparse
import config_factory
import site_config
from lib.data_loader import *

def main(keyword, debug):
    config = config_factory.load(False)
    master = master_site(config)
    video_data = master.global_site.video_data

    print("\nLocal search: %s" % keyword)
    has_result = False
    for id,video in video_data.items():
        match = False
        if keyword in video.title.lower():
            match = True
            if debug:
                print("- title: %s" % video.title)
        for tag in video.tags:
            if keyword in tag.lower():
                match = True
                if debug:
                    print("- tag: %s" % tag)
        if match:
            print("%s // %s" % (video.id, video.title))
            has_result = True
    if not has_result:
        print("No match")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Local search')
    parser.add_argument('keyword')
    parser.add_argument('--debug', default=False, action='store_true')
    args = parser.parse_args()
    main(args.keyword.lower(), debug = args.debug)
