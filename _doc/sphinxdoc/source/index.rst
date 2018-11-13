
.. |gitlogo| image:: _static/git_logo.png
             :height: 20

lightmlrestapi
==============

.. image:: https://travis-ci.org/sdpython/lightmlrestapi.svg?branch=master
    :target: https://travis-ci.org/sdpython/lightmlrestapi
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

.. image:: https://requires.io/github/sdpython/lightmlrestapi/requirements.svg?branch=master
     :target: https://requires.io/github/sdpython/lightmlrestapi/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://codecov.io/github/sdpython/lightmlrestapi/coverage.svg?branch=master
    :target: https://codecov.io/github/sdpython/lightmlrestapi?branch=master

.. image:: http://img.shields.io/github/issues/sdpython/lightmlrestapi.png
    :alt: GitHub Issues
    :target: https://github.com/sdpython/lightmlrestapi/issues

.. image:: https://badge.waffle.io/sdpython/lightmlrestapi.png?label=to%20do&title=to%20do
    :alt: Waffle
    :target: https://waffle.io/sdpython/lightmlrestapi

.. image:: nbcov.png
    :target: http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/all_notebooks_coverage.html
    :alt: Notebook Coverage

*lightmlrestapi* implements a light machine learning :epkg:`REST API`
based on :epkg:`falcon`.

.. toctree::
    :maxdepth: 1

    tutorial/index
    gyexamples/index
    api/index
    i_cmd
    i_ex
    all_notebooks
    blog/blogindex
    index_modules
    i_index

You can test a dummy :epkg:`wsgi` server by running:

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

The command line is described at
:ref:`cmd_start_mlrestapi_cmd <Creates an falcon application and starts it through a wsgi application>`.
The purpose is to start a :epkg:`REST API` based on a custom model.

::

    start_mlrestapi <filename.py>

``<filename>.py`` must contain a predict function described
as follows:

::

    import pickle

    # We declare an id for the REST API.
    def restapi_version():
        return "0.1.1234"

    # We declare a loading function.
    def restapi_load():
        with open("iris2.pickle", "rb") as f:
            loaded_model = pickle.load(f)
        return loaded_model

    # We declare a predict function.
    def restapi_predict(clf, X):
        return clf.predict_proba(X)

    # We test it works.
    if __name__ == "__main__":
        clf = restapi_load()
        print(restapi_predict(clf, [0.1, 0.2]))

**Links:** `github <https://github.com/sdpython/lightmlrestapi/>`_,
`documentation <http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/index.html>`_,
:ref:`l-README`,
:ref:`blog <ap-main-0>`

+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`l-modules`     |  :ref:`l-functions` | :ref:`l-classes`    | :ref:`l-methods`   | :ref:`l-staticmethods` | :ref:`l-properties`                            |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`modindex`      |  :ref:`l-EX2`       | :ref:`search`       | :ref:`l-license`   | :ref:`l-changes`       | :ref:`l-README`                                |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`genindex`      |  :ref:`l-FAQ2`      | :ref:`l-notebooks`  | :ref:`l-HISTORY`   | :ref:`l-statcode`      | `Unit Test Coverage <coverage/index.html>`_    |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
