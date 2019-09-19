import config_factory
from lib.data_loader import *

def dump_site(site):
    lines = []
    groups = sorted(site.groups, key = lambda group: group.title.lower())
    for group in groups:
        lines.append("# %s" % group.title)
        for id in group.ids:
            lines.append("%s // %s" % (id, site.video_data[id].title))
        lines.append("")
    return lines

def main():
    config = config_factory.load()
    master = master_site(config, merge_small_groups = False)
    
    for site in master.lang_sites.values():
        lines = dump_site(site)
        # write back to data file
        with open("data/%s/data.txt" % site.lang, "w") as f:
            f.write('\n'.join(lines))
            print("Updated %s" % f.name)

main()
