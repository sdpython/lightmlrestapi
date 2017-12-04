"""
@file
@brief Machine Learning Post request
"""
import falcon
from ..mlapp import MachineLearningPost


def dummy_application(app=None):
    """
    Defines a dummy application using this API.

    @param      app     application, if None, creates one
    @return             app

    You can start it by running:

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
    """
    from sklearn import datasets
    from sklearn.linear_model import LogisticRegression

    iris = datasets.load_iris()
    X = iris.data[:, :2]  # we only take the first two features.
    y = iris.target
    clf = LogisticRegression()
    clf.fit(X, y)

    if app is None:
        app = falcon.API()
    app.add_route('/', MachineLearningPost(clf.predict_proba))
    return app
