# -*- coding: utf-8 -*-
import sys
import os
import sphinx_readable_theme
from pyquickhelper.helpgen.default_conf import set_sphinx_variables, get_default_stylesheet

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))

local_template = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "phdoc_templates")

set_sphinx_variables(__file__, "lightmlrestapi", "Xavier Dupré", 2019,
                     "readable", sphinx_readable_theme.get_html_theme_path(),
                     locals(), extlinks=dict(
                         issue=('https://github.com/sdpython/lightmlrestapi/issues/%s', 'issue')),
                     title="lightmlrestapi", book=True)

blog_root = "http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/"

html_context = {
    'css_files': get_default_stylesheet() + ['_static/my-styles.css'],
}

html_logo = "project_ico.png"

html_sidebars = {}

language = "en"

mathdef_link_only = True

epkg_dictionary.update({
    'Apache': 'https://httpd.apache.org/',
    'API REST': 'https://en.wikipedia.org/wiki/Representational_state_transfer',
    'bjoern': "https://github.com/jonashaag/bjoern",
    'C': 'https://en.wikipedia.org/wiki/C_(programming_language)',
    'falcon': "https://falconframework.org/",
    'flask': "http://flask.pocoo.org/",
    'ImageNet': 'http://www.image-net.org/',
    'Iris dataset': 'http://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html',
    'iris dataset': 'http://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html',
    'json': 'https://docs.python.org/fr/3/library/json.html',
    'keras': 'https://keras.io/',
    'mod_wsgi': 'https://github.com/GrahamDumpleton/mod_wsgi',
    'POST': 'https://en.wikipedia.org/wiki/POST_(HTTP)',
    'PIL': ("https://pillow.readthedocs.io/en/4.3.x/",
            ("https://pillow.readthedocs.io/en/4.3.x/reference/{0}.html", 1),
            ("https://pillow.readthedocs.io/en/4.3.x/reference/{0}.html#PIL.{0}.{1}", 2)),
    'pyjwt': 'https://pyjwt.readthedocs.io/en/latest/index.html',
    'pytorch': 'https://pytorch.org/',
    'reservoir sampling': 'https://en.wikipedia.org/wiki/Reservoir_sampling',
    'REST API': "https://en.wikipedia.org/wiki/Representational_state_transfer",
    'pickle': 'https://docs.python.org/3/library/pickle.html',
    'torch': 'https://pytorch.org/',
    'urllib3': 'https://urllib3.readthedocs.io/en/latest/',
    'utf-8': 'https://en.wikipedia.org/wiki/UTF-8',
    'uwsgi': 'http://uwsgi-docs.readthedocs.io/en/latest/',
    'waitress': 'https://docs.pylonsproject.org/projects/waitress/en/latest/',
    'wsgi': 'https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface',
    'WSGI': 'https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface',
})
