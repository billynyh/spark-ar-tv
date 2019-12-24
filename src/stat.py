from lib.data_loader import *
import config_factory
import collections

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
            thresold = 2000
            if view_count > thresold:
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

from itertools import chain
def dump_lang_stat(master):
    video_data = master.global_site.video_data
    total = 0
    for key, site in master.lang_sites.items():
        num_vid = 0
        ids = []
        for g in site.groups:
            num_vid += len(g.ids)
            ids += g.ids
        total += num_vid
        dup = [item for item, count in collections.Counter(ids).items() if count > 1]
        if len(dup) > 0:
            print(dup)
        print("%s: %d %d" % (site.lang, num_vid, len(set(ids))))

    gsite = master.global_site
    for g in (gsite.facebook + gsite.music):
        num_vid = len(g.ids)
        total += num_vid
        dup = [item for item, count in collections.Counter(g.ids).items() if count > 1]
        if len(dup) > 0:
            print(dup)
        print("%s: %d %d" % (g.title, num_vid, len(set(g.ids))))
    print("Total: %d" % total)

    # find duplicated
    for k1, site1 in master.lang_sites.items():
        for k2, site2 in master.lang_sites.items():
            if k1 == k2: 
                continue
            ids1 = set(chain.from_iterable([g.ids for g in site1.groups]))
            ids2 = set(chain.from_iterable([g.ids for g in site2.groups]))
            dup = ids1.intersection(ids2)
            if len(dup) > 0:
                print("%s - %s" % (k1, k2))
                print(dup)
            

def main():
    config = config_factory.load(False)
    master = master_site(config)
    site = master.global_site
    groups = site.groups_by_time
    dump_groups_stat(groups, site.video_data)
    dump_groups_details(groups[1:6], site.video_data)
    dump_lang_stat(master)
    #dump_groups_ids(groups[1:6], site.video_data)

    print("All videos: %s" % len(site.video_data))

    dump_top_videos(site)

main()
