
.. l-dummy-function-application:

==========================
Create your first REST API
==========================

The module provides helpers to build a REST API
based on a function which computes predictions for
a machine learning model. The following steps
explains how to build a simple example.

.. contents::
    :local:

Train a model
=============

Let's train and save a simple model based on
`Iris datasets <http://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html>`_.

.. runpython::
    :showcode:

    import pickle
    from sklearn import datasets
    from sklearn.linear_model import LogisticRegression

    iris = datasets.load_iris()
    X = iris.data[:, :2]  # we only take the first two features.
    y = iris.target
    clf = LogisticRegression()
    clf.fit(X, y)
    with open("iris2.pickle", "wb") as f:
        pickle.dump(clf, f)

The model could be anything not from :epkg:`scikit-learn`
or any other machine learning library not even a model.

.. _l-mlapp-def:

Implement your predict function
===============================

The following function must be stored in a local file.
Let's choose ``mymlrestapi.py``.

.. runpython::
    :showcode:

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

Start the REST API server
=========================

We first run the server locally.
The command line :ref:`cmd_start_mlrestapi_cmd`:

::

    start_mlrestapi --name=dummyfct --options=mymlrestapi.py

Test the REST API
=================

The final test consists in checking we can obtain
the prediction by calling the server.

::

    import requests
    import ujson
    features = ujson.dumps({'X': [0.1, 0.2]})
    r = requests.post('http://127.0.0.1:8081', data=features)
    print(r)
    print(r.json())

REST API with authentification
==============================

To query the REST API with an authentified user:

::

    import requests
    import ujson
    features = ujson.dumps({'X': [0.1, 0.2]})
    r = requests.post('http://127.0.0.1:8081', data=features, protocol='https',
                      headers=dict(uid="user", token="password"))
    print(r)
    print(r.json())

The command line :ref:`cmd_start_mlrestapi_cmd` can launch the
application which requires authentification:

::

    start_mlrestapi --name=dummyfct --options=mymlrestapi.py --users=encrypted_passwords.txt

There is an first step which consists in encrypting the password
with command :ref:`cmd_encrypt4mlrestapi_cmd`.

::

    encrypt_pwd --input=users.txt --output=encrypted_passwords.txt
