
.. image:: https://travis-ci.com/sdpython/lightmlrestapi.svg?branch=master
    :target: https://app.travis-ci.com/github/sdpython/lightmlrestapi
    :alt: Build status

.. image:: https://ci.appveyor.com/api/projects/status/itkrtmperlhjm4xw?svg=true
    :target: https://ci.appveyor.com/project/sdpython/lightmlrestapi
    :alt: Build Status Windows

.. image:: https://circleci.com/gh/sdpython/lightmlrestapi/tree/master.svg?style=svg
    :target: https://circleci.com/gh/sdpython/lightmlrestapi/tree/master

.. image:: https://badge.fury.io/py/lightmlrestapi.svg
    :target: http://badge.fury.io/py/lightmlrestapi

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :alt: MIT License
    :target: http://opensource.org/licenses/MIT

.. image:: https://codecov.io/github/sdpython/lightmlrestapi/coverage.svg?branch=master
    :target: https://codecov.io/github/sdpython/lightmlrestapi?branch=master

.. image:: http://img.shields.io/github/issues/sdpython/lightmlrestapi.png
    :alt: GitHub Issues
    :target: https://github.com/sdpython/lightmlrestapi/issues

.. image:: http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/_images/nbcov.png
    :target: http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/all_notebooks_coverage.html
    :alt: Notebook Coverage

.. image:: https://img.shields.io/github/repo-size/sdpython/lightmlrestapi
    :target: https://github.com/sdpython/lightmlrestapi/
    :alt: size

.. _l-README:

lightmlrestapi
==============

It implements a light machine learning *REST API*
based on `falcon <https://falcon.readthedocs.io/en/stable/>`_.
If I were to start again this project, I would
probably choose `FastAPI <https://fastapi.tiangolo.com/>`_.
You can test a dummy *wsgi* server by running:

::

    start_mlrestapi --name=dummy

And then query it with:

::

    import requests
    import ujson
    features = ujson.dumps({'X': [0.1, 0.2]})
    r = requests.post('http://127.0.0.1:8081', data=features)
    print(r)
    print(r.json())

It should return:

::

    {'Y': [[0.4994216179, 0.4514893599, 0.0490890222]]}

The module was first tried with success in a hackathon in 2018.
Participants could upload their model and retrieve their predictions
through a REST API to check it was producing the same one as they had.
A simple way to put a model into production.

* `GitHub/lightmlrestapi <https://github.com/sdpython/lightmlrestapi/>`_
* `documentation <http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/index.html>`_
* `Blog <http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/blog/main_0000.html#ap-main-0>`_
