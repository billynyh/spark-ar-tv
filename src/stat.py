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
