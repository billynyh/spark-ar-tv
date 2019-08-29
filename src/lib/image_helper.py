from PIL import Image

from lib import util

def crop(img): # 16:9
    (w, h) = img.size
    h2 = w * 9 / 16
    if h > h2:
        diff = (h - h2) / 2
        (t, b) = (diff, h - diff)
    return img.crop((0, t, w, b))

def make_collage(r, c, paths):
    imgs = [crop(Image.open(path)) for path in paths]
    (w, h) = imgs[0].size
    size = (w*2, h*2)
    print(size)
    
    collage = Image.new('RGB', size)
    i = 0
    for img in imgs:
        x = i % c
        y = int(i / c)
        collage.paste(img, (x * w, y * h))
        i += 1
    return collage

def group_thumbnail_collage(site, ids):
    paths = [util.get_cache_image_path(id) for id in ids]
    return make_collage(2, 2, paths)

