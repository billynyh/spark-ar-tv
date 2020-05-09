
from lib.api import PlaylistApi
from lib.data_loader import *
import config_factory

def gen_playlist_from_group(api, g):
    playlist_id = api.create_playlist("Spark AR TV - %s" % g.title, g.title)
    add_group_to_playlist(api, g, playlist_id)

def add_group_to_playlist(api, g, playlist_id):
    i = 0
    for id in g.ids:
        api.add_video_to_playlist(playlist_id, i, id)
        i += 1

def main():
    config = config_factory.load(False)
    master = master_site(config)
    site = master.global_site
    groups = site.groups_by_week

    api = PlaylistApi()
    api.auth()

    # g = groups[6]:
    
    i = 0
    for g in site.topics:
        print("%d Spark AR TV - %s" % (i, g.title))
        i += 1

    print()
    #g = site.topics[16]
    g = groups[1]
    print(g.title)
    playlist_id = "PLJ-lx8QFIxZYuTqACE5t5V_iY2rase3Bn"
    add_group_to_playlist(api, g, playlist_id)

def main_url():
    config = config_factory.load(False)
    master = master_site(config)
    site = master.global_site
    groups = site.groups_by_week[:10]
    for g in groups:
        idx = 0
        chunks = util.chunks(g.ids, 50)
        for ids in chunks:
            idx += 1
            print('%s - %d' % (g.title, idx))
            print('http://www.youtube.com/watch_videos?video_ids=%s' % ','.join(ids))
            print()
    print("Steps:")
    print("https://webapps.stackexchange.com/questions/120451/how-to-create-a-playlist-form-a-list-of-links-not-from-bookmarks")

# main()
main_url()
