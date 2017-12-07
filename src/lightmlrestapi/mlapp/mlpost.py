"""
@file
@brief Machine Learning Post request
"""
import traceback
import json
import ujson
import falcon


class MachineLearningPost(object):
    """
    Implements a simple REST API which handles
    a post request, no authentification
    is required. The model ingests a vector *X*
    and outputs another one or a number *Y*.
    An basic exemple of an application is given by
    @see fn dummy_application.
    """

    def __init__(self, predict_function):
        """
        @param      predict_function    predict function
        """
        self._predict = predict_function

    def on_post(self, req, resp):
        """
        @param      req         request
        @param      resp        ...
        """
        # To get the parameters
        # req.get_params
        js = req.stream.read()
        args = ujson.loads(js)
        X = args["X"]
        try:
            res = self._predict([X])
        except Exception as e:
            excs = traceback.format_exc()
            es = str(e)
            if len(es) > 200:
                es = es[:200] + '...'
            raise falcon.HTTPBadRequest(
                'Unable to predict due to: {0}'.format(es), excs)

        resp.status = falcon.HTTP_201
        try:
            js = ujson.dumps({"Y": res})
        except OverflowError as e:
            try:
                json.dumps({"Y": res})
            except Exception as ee:
                raise OverflowError(
                    'res probably contains numpy arrays or numpy.types ({0}), they cannot be serialized.'.format(type(res))) from ee
            raise OverflowError(
                'res probably contains numpy arrays ({0}), they cannot be serialized with ujson but with json.'.format(type(res))) from e
        resp.body = js
