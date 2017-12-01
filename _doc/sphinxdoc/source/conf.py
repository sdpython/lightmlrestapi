#-*- coding: utf-8 -*-
import sys
import os
import datetime
import re
import sphinx_rtd_theme


sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.split(__file__)[0],
            "..",
            "..",
            "..",
            "..",
            "pyquickhelper",
            "src")))

local_template = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "phdoc_templates")

from pyquickhelper.helpgen.default_conf import set_sphinx_variables, get_default_stylesheet
set_sphinx_variables(__file__, "lightmlrestapi", "Xavier Dupré", 2017,
                     "sphinx_rtd_theme", [
                         sphinx_rtd_theme.get_html_theme_path()],
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

epkg_dictionary['Apache'] = 'https://httpd.apache.org/'
epkg_dictionary['mod_wsgi'] = 'https://github.com/GrahamDumpleton/mod_wsgi'
epkg_dictionary['falcon'] = "https://falconframework.org/"
epkg_dictionary['REST API'] = "https://en.wikipedia.org/wiki/Representational_state_transfer"
epkg_dictionary['uwsgi'] = 'http://uwsgi-docs.readthedocs.io/en/latest/'
epkg_dictionary['waitress'] = 'https://docs.pylonsproject.org/projects/waitress/en/latest/'
epkg_dictionary['wsgi'] = 'https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface'
