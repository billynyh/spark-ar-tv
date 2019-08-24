from const import *

HTML_BEFORE = """
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta property="og:image" content="assets/logo.png"/>

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="assets/style.css">

    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-39524040-2"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'UA-39524040-2');
    </script>


    <title>Spark AR TV</title>

  </head>
  <body>
    

<nav class="navbar navbar-dark bg-dark">
  <span class="navbar-brand">Spark AR TV</span>
  <ul class="navbar-nav mr-auto">
    <li class="nav-item">
      <a class="nav-link" href="https://forum.sparkar.wiki/d/94-spark-ar-tv-unofficial-video-tutorial-collections">Suggest content</a>
    </li>
   </ul>
</nav>

<div class="content">
<div class="container-fluid">
"""


HTML_AFTER = """


</div>
</div> 

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    <script>

/*
$(document).ready(function(){
});
*/

    </script>
  </body>
</html>

"""

def gen_header(group):
    return '<div class="row"><h3>%s</h3></div>' % group[TITLE]

def gen_video(obj):
    title = obj[TITLE]
    img = obj[THUMBNAIL_URL]
    url = "https://youtube.com/watch?v=%s" % obj[ID]
    channel = obj[CHANNEL_TITLE]
    return """
    <div class="vid-col col-xl-2 col-lg-3 col-sm-4">
    <div class="vid">
      <div class="thumb-container">
        <div class="thumb-wrapper">
          <a href="%(url)s" target="_blank">
            <img src="%(img)s">
            <span class="play-button">
              <img src="assets/youtube-play5.png" />
            </span>
          </a>
        </div>
        <span class="thumb-label">%(channel)s</span>
      </div>
      <div class="title">
        <a href="%(url)s">%(title)s</a>
      </div>
    </div>
    </div>""" % {'title': title, 'url':url, 'img':img, 'channel': channel}

def gen_group(group, video_data):
    video_list = group[LIST]

    html = []
    html.append(gen_header(group))
    html.append('<div class="row">')
    for vid in video_list:
        html.append(gen_video(video_data[vid]))
    html.append('</div>')
    
    return html

def gen_body(groups, video_data):
    html = []

    for group in groups:
        html += gen_group(group, video_data)

    return html

def gen_html(groups, video_data):
    html = [HTML_BEFORE]
    html += gen_body(groups, video_data)
    html.append(HTML_AFTER)
    return '\n'.join(html)
