
.. l-dummy-function-application:

==========================
Create your first REST API
==========================

The module provides helpers to build a REST API
based on a function which computes predictions for
aa machine learning model. The following steps
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

Implement your predict function
===============================

The following function must be stored in a local file.
Let's choose ``mymlrestapi.py``.

.. runpython::
    :showcode:

    import pickle

    # We load the model
    with open("iris2.pickle", "rb") as f:
        loaded_model = pickle.load(f)

    # We declare a predict function.
    def restapi_predict(X):
        return clf.predict_proba(X)

    # We test it works.
    if __name__ == "__main__":
        print(restapi_predict([0.1, 0.2]))

Start the REST API server
=========================

We first run the server locally.
The command line :ref:`start_mlrestapi`:

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
