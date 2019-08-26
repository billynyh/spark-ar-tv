from mako.template import Template
from mako.lookup import TemplateLookup

from lib.const import *
from lib import data_loader
from lib import util

def get_youtube_url(id):
    return "https://youtube.com/watch?v=%s" % id

def gen_video(video):

    t = get_template("_standard_video.html")
    return t.render(
        title = video.title, 
        url = video.video_url,
        img = video.thumbnail_url,
        channel = video.channel_title,
        duration = video.duration,
        published_at = video.published_at,
        channel_url = video.channel_url,
    )

def gen_group(group, video_data):
    video_list = group[LIST]

    html = []
    for vid in video_list:
        html.append(gen_video(video_data[vid]))
    t = get_template("_group.html")
    return t.render(title = group[TITLE], content = '\n'.join(html))

def gen_badge(text, cls):
    t = get_template("_featured_badge.html")
    return t.render(cls = cls, text = text)

# 7-col
def gen_featured(site):
    most_viewed = site.most_viewed
    video_data = site.video_data

    t = get_template("_featured_banner.html")
    return [t.render(videos=[video_data[id] for id in most_viewed[0:8]])]

def gen_channel_groups(groups, video_data):
    html = []
    html.append("""
        <div class="content">
        <div class="container-fluid">
        """)
    for group in groups:
        html.append(gen_group(group, video_data))
    html.append('</div></div>')

    return html

def gen_debug(video_data):
    (most_viewed, latest) = data_loader.sort_videos(video_data)

    NUM = 18
    debug_groups = [
      {TITLE: "Latest", LIST: latest[:NUM]},
      {TITLE: "Most Viewed", LIST: most_viewed[:NUM]},
    ]

    dump_video_list = ["# Latest"]
    dump_video_list += util.dump_video_list(latest[:NUM], video_data)
    dump_video_list += ["", "# Most viewed"]
    dump_video_list += util.dump_video_list(most_viewed[:NUM], video_data)

    html = [
      '<textarea style="width:50%%; height:400px">%s</textarea>' % '\n'.join(dump_video_list)
    ]
    html += gen_channel_groups(debug_groups, video_data)
    return html

def get_template(filename):
    lookup = TemplateLookup(directories=['.'])
    t = Template(filename="layouts/%s" % filename, lookup=lookup)
    return t

def gen_channel_html(site, debug = False):
    html = []
    if debug:
        html += gen_debug(site.video_data)
    html += gen_channel_groups(site.groups, site.video_data)

    t = get_template('channels.html')
    return t.render(content = '\n'.join(html))

def gen_timeline_html(site):
    html = []
    html += gen_featured(site)
    html += gen_channel_groups(site.groups_by_time, site.video_data)

    t = get_template('index.html')
    return t.render(content = '\n'.join(html))

