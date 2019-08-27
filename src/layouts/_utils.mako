<%def name="wrap(path)">${context.get('relative_path', '.')}/${path}</%def>
<%def name="asset(f)">${wrap("assets/%s" % f)}</%def>
