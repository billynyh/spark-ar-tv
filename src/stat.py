from lib.data_loader import *
from lib import nav_helper
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
        ids = group.ids.copy()
        ids.reverse()

        for x in ids:
            v = video_data[x]
            view_count = int(v.view_count)
            thresold = 100
            if view_count > thresold:
                print("%s // %s | %s" % (v.id, v.title, v.view_count))
                #print("%s %s\n%s\n" % (v.title, v.channel_title, v.video_url))
        print()

def dump_monthly_stat(video_data):
    stat = {}
    for m in [7,8,9,10,11]:
        st = datetime.date(2019, m, 1)
        ed = datetime.date(2019, m+1, 1)
        stat[m] = filter_video_by_date(video_data, st, ed)
            
    st = datetime.date(2019, 12, 1)
    ed = datetime.date(2020, 1, 1)
    stat[12] = filter_video_by_date(video_data, st, ed)

    for m in stat:
        print("%d: %d" % (m, len(stat[m])))

def format(s):
    val = int(s)
    if val > 1000:
        return "%dk" % (val / 1000)
    if val > 1000000:
        return "%.1fM" % (val / 1000000.0)
    return val

def dump_top_videos(site):
    all_ids = list(site.video_data.keys())
    all_ids = sorted(all_ids, key=lambda id: (int(site.video_data[id].view_count)), reverse=True)


    excludes = site.music[0].ids + ['rpSSbBqLshg']
    rank = 1
    for i in range(20):
        id = all_ids[i]
        if id in excludes:
            continue
        v = site.video_data[all_ids[i]]
        print("%s | %s | [%s](https://youtube.com/watch?v=%s)" % (format(v.view_count), v.channel_title, v.title, v.id))
        #top_video_html(v, rank)
        rank += 1

        if rank == 6:
            print('<h2>#6 - #10</h2>')

        if rank > 10:
            break

def top_video_html(v, rank):
    url = "https://youtube.com/watch?v=%s" % v.id
    print('<div class="row"><div class="col-12">')
    
    if rank <= 5:
        print('<span><em>#%d - %s | %s | Published at: %s</em></span><h5><a href="%s" target="_blank">%s</a></h5>' % (rank, format(v.view_count), v.channel_title, v.published_at, url, v.title))
        iframe = """<p><iframe width="800" height="450" src="https://www.youtube.com/embed/%s" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></p>""" % v.id
        print(iframe)
        print('<hr/>')
    else:
        print('<p><em>#%d - %s | %s<em/><br/><a href="%s">%s</a></p>' % (rank, format(v.view_count), v.channel_title, url, v.title))
        
    print("</div></div>")

from itertools import chain
def dump_lang_stat(master):
    stat = []
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
        stat.append({'lang': site.lang, 'num_videos': num_vid})
    stat = sorted(stat, key = lambda s: -s['num_videos'])

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
    return stat

def dump_channel_stat(site, video_data):
    print()
    print("== channel stat ==")
    results = []
    for g in site.groups:
        l = len(g.ids)
        if l > 10:
            first_vid = video_data[g.ids[0]]
            c = {
              'title': g.title,
              'num_videos': l,
              'combined_views': sum([int(video_data[id].view_count) for id in g.ids]),
              'url': 'https://youtube.com/channel/%s' % first_vid.channel_id,
              'channel_id': first_vid.channel_id,
            }
            results.append(c)
    results = sorted(results, key = lambda c: -c['num_videos'])
    rank = 0
    for c in results:
        rank += 1
        print("%s # %s" % (c['channel_id'],  c['title']))
        #print("#%d | %s videos\n%s\n%s" % (rank, c['num_videos'], c['title'], c['url']))

    print()
    print(" ".join([c['channel_id'] for c in results]))
    return results

def stat_html(stat):
    langs = stat['langs']
    rank = 0
    html = []
    for lang in langs[:5]:
        rank += 1
        num_videos = lang['num_videos']
        title = nav_helper.LANG_DISPLAY_NAME[lang['lang']]
        html += ['#%d | %s | %d videos' % (rank, title, num_videos)]
    return '\n'.join(html)

def main():
    config = config_factory.load(False)
    master = master_site(config)
    site = master.global_site
    groups = site.groups_by_time
    dump_groups_stat(groups, site.video_data)
    dump_groups_details(groups[0:4], site.video_data)

    stat = {}
    #stat['langs'] = dump_lang_stat(master)
    #dump_groups_ids(groups[1:6], site.video_data)

    print("All videos: %s" % len(site.video_data))

    #dump_top_videos(site)
    #dump_monthly_stat(site.video_data)
    
    #dump_channel_stat(site, site.video_data)
    #html = stat_html(stat)
    #print(html)

main()
