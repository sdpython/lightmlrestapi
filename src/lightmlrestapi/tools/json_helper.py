"""
@file
@brief Helpers about :epkg:`json`.
"""
import pprint
import numpy
import ujson


class JsonError(ValueError):
    """
    Raised when serialization to json does not work.
    """

    def __init__(self, obj, data=None):

        msg = pprint.pformat(obj)
        if len(msg) > 2000:
            msg = msg[:2000] + "\n..."
        msg2 = pprint.pformat(data)
        if len(msg2) > 2000:
            msg2 = msg2[:2000] + "\n..."
        ValueError.__init__(
            self, "Unable to serialize object of type '{}' into json.\n{}\n----\n{}".format(
                type(obj), msg, msg2))


def json_dumps(obj):
    """
    Dumps an object into :epkg:`json`.

    @param      X       object
    @return             json
    """
    if isinstance(obj, numpy.ndarray):
        data = dict(shape=obj.shape, dtype=str(obj.dtype),
                    data=obj.tolist(), ___=1)
        try:
            return ujson.dumps(data)
        except UnicodeDecodeError:
            raise JsonError(obj, data)
    return ujson.dumps(obj)


def json_loads(jsdata):
    """
    Loads an object from :epkg:`json`.

    @param      jsdata      json
    @return                 object
    """
    obj = ujson.loads(jsdata)
    if isinstance(obj, dict) and '___' in obj:
        # numpy array
        shape = obj['shape']
        obj = numpy.array(obj['data'], dtype=obj['dtype'])
        obj = obj.reshape(tuple(shape))
    return obj
