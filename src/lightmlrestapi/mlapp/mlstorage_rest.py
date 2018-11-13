"""
@file
@brief Machine Learning Post request
"""
import traceback
import json
import falcon
import numpy
import ujson
from .base_logging import BaseLogging


class MLBoardUpload(BaseLogging):
    """
    Implements a simple :epkg:`REST API` to
    upload, download zip files.
    """

    def __init__(self, secret=None, folder='.',
                 version=None):
        """
        @param      secret              see @see cl BaseLogging
        @param      folder              see @see cl BaseLogging
        @param      version             API REST version
        """
        BaseLogging.__init__(self, secret=secret, folder=folder)
        self._version = version

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
        add_log_data = dict(user=req.get_header('uid'), ip=req.access_route)
        if self._version is not None:
            add_log_data = self._version

        # To get the parameters
        # req.get_params
        try:
            js = req.stream.read()
        except AssertionError as e:
            excs = traceback.format_exc()
            es = str(e)
            if len(es) > 200:
                es = es[:200] + '...'
            log_data = dict(error=str(e))
            log_data.update(add_log_data)
            if self._load_params:
                log_data['load_params'] = self._load_params
            self.error("ML.load", log_data)
            raise falcon.HTTPBadRequest(
                'Unable to retrieve request content due to: {0}'.format(es), excs)

        args = ujson.loads(js)
        self.save_time()
        duration = self.duration()
        log_data = dict(duration=duration)
        self.info("MLB.load", log_data)

        self.save_time()
        res = self._store(args)
        log_data = dict(duration=duration)
        self.info("MLB.store", log_data)

        resp.status = falcon.HTTP_201
        answer = {"name": res["name"]}
        try:
            js = ujson.dumps(answer)
        except OverflowError as e:
            try:
                json.dumps(answer)
            except Exception as ee:
                raise OverflowError(
                    'res probably contains numpy arrays or numpy.types ({0}), they cannot be serialized.'.format(type(res))) from ee
            raise OverflowError(
                'res probably contains numpy arrays ({0}), they cannot be serialized with ujson but with json.'.format(type(res))) from e
        resp.body = js
