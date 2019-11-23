from lib.data_loader import *
import config_factory


def dump_groups_stat(groups, video_data):
    for group in groups:
        num_vid = len(group.ids)
        num_channels = len(set([video_data[id].channel_id for id in group.ids]))
        print("%s: %s videos, %s channels" % (group.title, num_vid, num_channels))

def dump_groups_ids(groups, video_data):
    for group in groups:
        print(group.title)
        print(' '.join(group.ids))
        print()

def dump_groups_details(groups, video_data):
    for group in groups:
        print(group.title)
        for x in group.ids:
            v = video_data[x]
            view_count = int(v.view_count)
            if view_count > 2000:
                print("%s // %s | %s" % (v.id, v.title, v.view_count))
        print()

def dump_top_videos(site):
    all_ids = list(site.video_data.keys())
    all_ids = sorted(all_ids, key=lambda id: (int(site.video_data[id].view_count)), reverse=True)

    def format(s):
        val = int(s)
        if val > 1000:
            return "%dk" % (val / 1000)
        return val

    for i in range(20):
        v = site.video_data[all_ids[i]]
        print("%s | %s | [%s](https://youtube.com/watch?v=%s)" % (format(v.view_count), v.channel_title, v.title, v.id))


def main():
    config = config_factory.load(False)
    master = master_site(config)
    site = master.global_site
    groups = site.groups_by_time
    dump_groups_stat(groups, site.video_data)
    #dump_groups_details(groups[1:6], site.video_data)
    dump_groups_ids(groups[1:6], site.video_data)

    print("All videos: %s" % len(site.video_data))

    dump_top_videos(site)

main()
