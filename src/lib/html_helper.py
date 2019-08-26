from mako.template import Template
from mako.lookup import TemplateLookup

from lib.const import *
from lib import data_loader
from lib import util

def get_youtube_url(id):
    return "https://youtube.com/watch?v=%s" % id

def gen_video(obj):
    title = obj[TITLE]
    img = obj[THUMBNAIL_URL]
    url = get_youtube_url(obj[ID])
    channel = obj[CHANNEL_TITLE]
    duration = obj[DURATION]
    published_at = obj[PUBLISHED_AT]
    channel_url = "https://www.youtube.com/channel/%s" % obj[CHANNEL_ID]

    t = get_template("_standard_video.html")
    return t.render(
        title = title, 
        url = url,
        img = img,
        channel = channel,
        duration = duration,
        published_at = published_at,
        channel_url = channel_url,
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

    hot_badge = gen_badge("HOT", "badge-hot")

    html = []
    html.append("""
        <div class="container-fluid featured">
        <div class="row">
        """)
    html += gen_featured_big_col(most_viewed[0], video_data, hot_badge)
    html += gen_featured_col(most_viewed[1:3], video_data, hot_badge)
    html += gen_featured_col(most_viewed[3:5], video_data, hot_badge)
    html += gen_featured_big_col(most_viewed[5], video_data)
    html += gen_featured_col(most_viewed[6:8], video_data)
    html.append('</div></div>')

    return html

def gen_featured_big_col(id, video_data, badge = ""):
    html = [
        '<div class="featured-col-2">',
        gen_featured_video(video_data[id], badge),
        '</div>'
    ]
    return html

def gen_featured_col(ids, video_data, badge = ""):
    html = [
        '<div class="featured-col-1">',
        gen_featured_video(video_data[ids[0]], badge),
        gen_featured_video(video_data[ids[1]], badge),
        '</div>'
    ]
    return html

def gen_featured_video(obj, badge):
    t = get_template("_featured_video.html")
    return t.render(
        img = obj[THUMBNAIL_URL], 
        badge = badge,
        title = obj[TITLE],
        channel = obj[CHANNEL_TITLE],
        published_at = obj[PUBLISHED_AT],
        url = get_youtube_url(obj[ID]),
    )

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
