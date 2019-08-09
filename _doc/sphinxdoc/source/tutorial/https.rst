
.. _l-https:

===================
REST API with HTTPS
===================

Any solutions seemed to be working to enable
https on Windows with :epkg:`falcon`. Every
documented example implied linux and the easiest
one seems to be with :epkg:`uwsgi`.

.. contents::
    :local:

First application with uwsgi
============================

Let's follow this instructions described on the documentation
`The first WSGI application
<https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html>`_.
The file ``firstapp.py``:

::

    def application(env, start_response):
        start_response('200 OK', [('Content-Type','text/html')])
        return [b'Hello World']

Let's create an INI file ``firstapp.ini``:

::

    [uwsgi]
    http = <IPADDRESS>:8878
    wsgi-file = firstapp.py
    processes = 4
    threads = 2
    master

And we need to enable port *8878*:

::

    sudo ufw allow 8878

And finally the command line to run:

::

    uwsgi firstapp.ini

It works.

Second application falcon + uwsgi
=================================

Let's create the file ``secondapp.py``.

::

    import falcon
    import ujson

    class QuoteResource:

        def on_get(self, req, resp):
            quote = {
                'quote': (
                    'I\'ve always been more interested in '
                    'the future than in the past.'
                ),
                'author': 'Grace Hopper'
            }

            resp.body = ujson.dumps(quote)
            resp.status = falcon.HTTP_200

    app = falcon.API()
    app.add_route('/', QuoteResource())

Let's create an INI file ``secondapp.ini``:

::

    [uwsgi]
    http = <IPADDRESS>:8878
    wsgi-file = secondapp.py
    callable = app
    processes = 4
    threads = 2
    master

The final command line:

::

    uwsgi secondapp.ini

Third application: falcon + wsgi + https
========================================

We look into a the same application but deployed through the
*https* protocol. We first need to generate a certificate:

::

    openssl genrsa -out thirdapp.key 2048
    openssl req -new -key thirdapp.key -out thirdapp.csr
    openssl x509 -req -days 365 -in thirdapp.csr -signkey thirdapp.key -out thirdapp.crt

Let's create an INI file ``thirdadd.ini``:

::

    [uwsgi]
    https = <IPADDRESS>:8878,thirdadd.crt,thirdadd.key
    wsgi-file = secondapp.py
    callable = app
    processes = 4
    threads = 2
    master

Still the final command line:

::

    uwsgi thirdapp.ini

The url ``https://<IPADDRESS>:8878`` returns the content.

Fourth application: falcon + wsgi + https + scikit-learn
========================================================

The full application to serve predictions with a
:epkg:`scikit-learn` model. Let's first create a model:

.. runpython::
    :showcode:

    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier
    import pickle

    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    dt = DecisionTreeClassifier()
    dt.fit(X_train, y_train)

    with open('dtiris.pkl', 'wb') as f:
        pickle.dump(dt, f)

    print(dt)

The REST API is given by the following and save in
``fourt

::

    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier
    import falcon
    import pickle

    def load_model():
        with open('dtiris.pkl', 'rb') as f:
            dt = pickle.load(f)
        return dt

    from lightmlrestapi.mlapp import MachineLearningPost
    handler = MachineLearningPost(load_function=load_model,
                                  predict_function=lambda mod, X: mod.predict_proba(X))

    app = falcon.API()
    app.add_route('/', handler)

And the INI file ``fourthapp.ini``
(we reuse the same certificate):

::

    [uwsgi]
    https = <IPADDRESS>:8878,thirdadd.crt,thirdadd.key
    wsgi-file = fourthapp.py
    callable = app
    processes = 4
    threads = 2
    master

Still the final command line:

::

    uwsgi fourthapp.ini

Let's try the REST API:

::

    import requests
    import ujson
    features = ujson.dumps({'X': [0.1, 0.2]})
    r = requests.post('https://<IPADDRESS>:8878', data=features,
                      verify=False)
    print(r)
    print(r.json())

Parameter ``verify=False`` is explained at
`SSL Cert Verification
<https://2.python-requests.org/en/master/user/advanced/#ssl-cert-verification>`_.
