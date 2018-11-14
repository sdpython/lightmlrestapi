"""
@file
@brief Machine Learning Post request
"""
import traceback
import falcon
import numpy
import ujson
from .base_logging import BaseLogging
from .mlstorage import MLStorage
from ..args.args_images import string2bytes


class MLStoragePost(BaseLogging):
    """
    Implements a simple :epkg:`REST API` to
    upload zip files.
    """

    def __init__(self, secret=None, folder='.',
                 folder_storage='.', version=None):
        """
        @param      secret              see @see cl BaseLogging
        @param      folder              see @see cl BaseLogging
        @param      folder_storage      see @see cl MLStorage
        @param      version             API REST version
        """
        BaseLogging.__init__(self, secret=secret, folder=folder)
        self._storage = MLStorage(folder_storage)
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

        command = args.pop('cmd', None)
        if command == 'upload':

            self.save_time()
            name = self._store(args)
            log_data = dict(duration=duration)
            self.info("MLB.store", log_data)

            resp.status = falcon.HTTP_201
            answer = {"name": name}
        elif command == 'predict':
            raise NotImplementedError("cannot predict")
        else:
            es = "Unknown command '{0}'".format(command)
            log_data = dict(msg=es)
            if self._load_params:
                log_data['load_params'] = self._load_params
            self.error("MLStorage", log_data)
            raise falcon.HTTPBadRequest(
                'Unable to retrieve request content due to: {0}'.format(es))

        try:
            js = ujson.dumps(answer)
        except OverflowError as e:
            raise OverflowError('Answer cannot be serialized.') from e
        resp.body = js

    def _store(self, args):
        """
        Stores the model in the storage.
        """
        name = args.pop('name', None)
        if name is None:
            raise KeyError("Unable to find a model name")
        keys = list(args.keys())
        for k in keys:
            args[k] = string2bytes(args[k])
        self._storage.add(name, args)
        return name
