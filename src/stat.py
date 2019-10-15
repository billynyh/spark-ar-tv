from lib.data_loader import *
import config_factory

config = config_factory.load(False)
master = master_site(config)
site = master.global_site
groups = site.groups_by_time
for group in groups:
    num_vid = len(group.ids)
    num_channels = len(set([site.video_data[id].channel_id for id in group.ids]))
    print("%s: %s videos, %s channels" % (group.title, num_vid, num_channels))

print("All videos: %s" % len(site.video_data))

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
