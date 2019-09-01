
def wrap(context, path):
    return "%s/%s" % (context.get('site').url, path)

def asset(context, path):
    return wrap(context, "assets/%s" % path)

