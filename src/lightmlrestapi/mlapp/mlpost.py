"""
@file
@brief Machine Learning Post request
"""
import traceback
import json
import ujson
import falcon
import logging
import logging.handlers
import numpy
from .base_logging import BaseLogging


class MachineLearningPost(BaseLogging):
    """
    Implements a simple :epkg:`REST API` which handles
    a post request, no authentification
    is required. The model ingests a vector *X*
    and outputs another one or a number *Y*.
    An basic exemple of an application is given by
    @see fn dummy_application.
    """

    def __init__(self, predict_function, secret=None, folder='.',
                 log_features=True, log_prediction=True):
        """
        @param      predict_function    predict function
        @param      secret              see @see cl BaseLogging
        @param      folder              see @see cl BaseLogging
        @param      log_features        log the features
        @param      log_prediction      log the prediction
        """
        BaseLogging.__init__(self, secret=secret, folder=folder)
        self._predict = predict_function
        self._log_features = log_features
        self._log_prediction = log_prediction
    
    @staticmethod
    def data2json(data):
        """
        :epkg:`numpy:array` cannot be converted into
        :epkg:`json`. We change the type into a list.
        """
        if isinstance(data, numpy.ndarray):
            return dict(shape=data.shape, data=data.tolist())
        else:
            return data

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
        self.save_time()
        try:
            res = self._predict([X])
        except Exception as e:
            excs = traceback.format_exc()
            es = str(e)
            if len(es) > 200:
                es = es[:200] + '...'
            raise falcon.HTTPBadRequest(
                'Unable to predict due to: {0}'.format(es), excs)
        duration = self.duration()
        
        self.save_time()
        log_data = {'duration': duration}
        if self._log_features:
            log_data['X'] = MachineLearningPost.data2json(X)
        if self._log_prediction:
            log_data['Y'] = MachineLearningPost.data2json(res)
        duration_log = self.duration()
        log_data['logging'] = duration_log
        self.info("ML", log_data)
        
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
