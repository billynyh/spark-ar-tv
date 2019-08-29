
def wrap(context, path):
    return "%s/%s" % (context.get('relative_path', '.'), path)

def asset(context, path):
    return wrap(context, "assets/%s" % path)

