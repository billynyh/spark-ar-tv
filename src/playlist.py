
from lib.api import PlaylistApi
from lib.data_loader import *
import config_factory

def gen_playlist_from_group(api, g):
    playlist_id = api.create_playlist("Spark AR TV - %s" % g.title, g.title)

    i = 0
    for id in g.ids:
        api.add_video_to_playlist(playlist_id, i, id)
        i += 1

def main():
    config = config_factory.load(False)
    master = master_site(config)
    site = master.global_site
    groups = site.groups_by_time

    api = PlaylistApi()
    api.auth()

    st = 6
    ed = st + 1
    for g in groups[st:ed]:
        print(g.title)
        gen_playlist_from_group(api, g)
        


main()
