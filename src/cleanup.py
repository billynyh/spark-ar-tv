import config_factory
from site_config import DEVELOPER_KEY
from lib import util
from lib.api import ApiDataLoader
from lib.data_loader import *
from numpy import unique

def dump_site(site):
    data_dir = "data/%s" % site.lang
    skip_ids = set(load_skip_ids(data_dir))

    groups = regroup_by_channel(site.groups, site.video_data, skip_ids)
    groups = sorted(groups, key = lambda group: group.title.lower())
    fix_title = True
    return dump_groups(groups, site.video_data, fix_title)

def dump_groups(groups, video_data, fix_title):
    lines = []
    for group in groups:
        if len(group.ids) == 0:
            continue
        ids = sorted(group.ids, key = lambda id: (video_data[id].raw_published_at, id))
        appeared = set()
        if fix_title:
            group_title = video_data[ids[0]].channel_title
        else:
            group_title = group.title
        lines.append("# %s" % group_title)
        for id in ids:
            if id in appeared:
                continue
            if video_data[id].live_broadcast_content == 'upcoming':
                print('%s is upcoming' % id)
                util.delete_cache_json(id)
                continue
            appeared.add(id)
            lines.append("%s // %s" % (id, video_data[id].title))
        lines.append("")
    return lines

def regroup_by_channel(groups, video_data, skip_ids):
    lines = []
    ids = []
    for group in groups:
        ids += group.ids
    channels = {}
    for id in ids:
        if id in skip_ids:
            continue
        v = video_data[id]
        c = v.channel_id
        if not channels.get(c, None):
            channels[c] = []
        channels[c].append(id)
    new_groups = [Group(video_data[ids[0]].channel_title, ids) for (c, ids) in channels.items()]
    return new_groups

def cleanup_custom_groups(groups, video_data, fname):
    fix_title = False
    lines = dump_groups(groups, video_data, fix_title)
    with open("data/%s" % fname, "w") as f:
        f.write('\n'.join(lines))
        print("Updated %s" %  f.name)


def cleanup(master):
    
    for site in master.lang_sites.values():
        lines = dump_site(site)
        # write back to data file
        with open("data/%s/data.txt" % site.lang, "w") as f:
            f.write('\n'.join(lines))
            print("Updated %s" % f.name)

    video_data = master.global_site.video_data
    cleanup_custom_groups(master.global_site.facebook, video_data, "facebook.txt")
    cleanup_custom_groups(master.global_site.topics, video_data, "topics.txt")

def main():
    util.prepare_cache()
    config = config_factory.load()
    master = master_site(config, merge_small_groups = False)
    cleanup(master)

if __name__=="__main__":
    main()
    #main()
