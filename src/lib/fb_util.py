import urllib.parse


IFRAME_FS = """
<iframe src="https://www.facebook.com/plugins/video.php?href=%(escaped_url)s&width=%(width)d&show_text=true&appId=%(app_id)s&height=%(height)d" width="%(width)d" height="%(height)d" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowTransparency="true" allow="encrypted-media" allowFullScreen="true"></iframe>
"""

def get_iframe_html(url, app_id, width=800, height=532):
    return IFRAME_FS % {'escaped_url': urllib.parse.quote(url, safe=''), 'app_id': app_id, 'width': width, 'height': height}

