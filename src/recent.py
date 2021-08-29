import config_factory
from lib.data_loader import *

def main():
    config = config_factory.load()
    master = master_site(config, merge_small_groups = False)
    site = master.global_site
    ids = [id for g in site.groups_by_day[:10] for id in g.ids]
    print('\n'.join(ids))

if __name__=="__main__":
    main()
