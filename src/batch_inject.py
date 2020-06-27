import config_factory
import cleanup

from lib.model import MasterSite, Site, Group, ChannelList
from lib import util
from lib.data_loader import *


def parse(lines):
    group_map = {}
    current_group = None
    for s in lines:
        s = s.strip()
        if not s:
            continue
        if s.startswith("#"):
            if current_group:
                group_map[current_group.title] = current_group
            current_group = Group(title = s[1:].strip(), ids = [])
            continue

        current_group.ids.append(util.extract_youtube_id(s))
    if current_group: 
        group_map[current_group.title] = current_group
    
    return group_map

def main():
    util.prepare_cache()
    config = config_factory.load()
    master = master_site(config, merge_small_groups = False)
    new_data = parse(open("input.txt").readlines())
    for (lang, site) in master.lang_sites.items():
        if new_data.get(lang, None):
            groups = site.groups + [new_data[lang]]

            lines = []
            for group in groups:
                lines.append("# %s" % group.title)
                for id in group.ids:
                    lines.append("%s" % id)
                lines.append("")
            with open("data/%s/data.txt" % site.lang, "w") as f:
                f.write('\n'.join(lines))
                print("Updated %s" % f.name)
    
    cleanup.main()

if __name__=="__main__":
    main()
