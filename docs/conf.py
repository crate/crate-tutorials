from crate.theme.rtd.conf.crate_tutorials import *


if "sphinx.ext.intersphinx" not in extensions:
    extensions += ["sphinx.ext.intersphinx"]


if "intersphinx_mapping" not in globals():
    intersphinx_mapping = {}


intersphinx_mapping.update({
    'reference': ('https://crate.io/docs/crate/reference/', None),
    'howtos': ('https://crate.io/docs/crate/howtos/', None),
    'admin-ui': ('https://crate.io/docs/crate/admin-ui/', None),
    'crash': ('https://crate.io/docs/crate/crash/', None),
    })
