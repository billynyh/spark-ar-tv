import config_factory
from site_config import DEVELOPER_KEY
from lib.api import ApiDataLoader
from lib.data_loader import *
from numpy import unique

def dump_site(site):
    groups = sorted(site.groups, key = lambda group: group.title.lower())
    return dump_groups(groups, site.video_data)

def dump_groups(groups, video_data):
    lines = []
    for group in groups:
        lines.append("# %s" % group.title)
        ids = sorted(group.ids, key = lambda id: (video_data[id].raw_published_at, id))
        appeared = set()
        for id in ids:
            if id in appeared:
                continue
            appeared.add(id)
            lines.append("%s // %s" % (id, video_data[id].title))
        lines.append("")
    return lines

def cleanup_groups(groups, video_data, fname):
    lines = dump_groups(groups, video_data)
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
    cleanup_groups(master.global_site.facebook, video_data, "facebook.txt")
    cleanup_groups(master.global_site.topics, video_data, "topics.txt")

def main():
    config = config_factory.load()
    master = master_site(config, merge_small_groups = False)
    cleanup(master)

if __name__=="__main__":
    main()