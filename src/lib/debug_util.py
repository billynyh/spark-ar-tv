from lib import data_loader
from lib import util
from lib.model import Group

def get_message(site):
    video_data = site.video_data
    (most_viewed, latest) = data_loader.sort_videos(video_data)

    NUM = 18
    debug_groups = [
      Group("Latest", latest[:NUM]),
      Group("Most Viewed", most_viewed[:NUM]),
    ]

    dump_video_list = ["# Latest"]
    dump_video_list += util.dump_video_list(latest[:NUM], video_data)
    dump_video_list += ["", "# Most viewed"]
    dump_video_list += util.dump_video_list(most_viewed[:NUM], video_data)

    debug_text = '\n'.join(dump_video_list)
