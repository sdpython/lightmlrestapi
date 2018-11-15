"""
@file
@brief Helpers to submit REST API requests.
"""
import os
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
import ujson
from ..args import zip_dict, bytes2string


def json_upload_model(name, pyfile, data=None):
    """
    Builds a REST request to upload a machine learned models to a REST API defined by
    @see cl MLStoragePost.

    :param name: name of the model, should be unique and not already used
    :param pyfile: python file which computes the prediction,
        the file must follows the specification defined in
        :ref:`l-template-ml`
    :param data: binary file, usually everything the models pickled
    :param host: ip address of the application
    :param port: port
    :param fLOG: logging function
    :return: json as a dictionary ready to be jsonify (with ``ujson.dumps(request)``)
    """
    if name is None or name == '':
        raise ValueError("name cannot be empty.")
    if not os.path.exists(pyfile):
        raise FileNotFoundError("Unable to find '{0}'.".format(pyfile))
    if data and not os.path.exists(data):
        raise FileNotFoundError("Unable to find '{0}'.".format(data))

    # model file
    last_file = os.path.split(pyfile)[-1]
    with open(pyfile, "rb") as f:
        code = f.read()

    if code == '':
        raise ValueError("File '{0}' cannot be empty.".format(pyfile))
    model_data = {last_file: code}

    # model data
    if data:
        last_data = os.path.split(data)[-1]
        with open(data, "rb") as f:
            content = f.read()
        model_data[last_data] = content

    # zip data
    zipped = zip_dict(model_data)
    request = dict(name=name, cmd='upload',
                   zip=bytes2string(zipped))
    return request


def submit_rest_request(request, login=None, pwd=None, url='http://127.0.0.1:8081/',
                        timeout=15, fLOG=None):
    """
    Submits a request to a REST API defined by
    @see cl MLStoragePost.

    :param login: login
    :param pwd: password
    :param request: request as a dictionary
    :param host: host
    :param port: port
    :param timeout: timeout
    :param fLOG: logging function
    :return: request results as dictionary
    """
    if login:
        if fLOG:
            fLOG("[submit_rest_request] submit authentified request as '{0}' to '{1}'".format(
                login, url))
        auth = HTTPBasicAuth(login, pwd)
        jsonified = ujson.dumps(request)
        response = requests.post(
            url, auth=auth, data=jsonified, timeout=timeout)
    else:
        if fLOG:
            fLOG("[submit_rest_request] submit request to '{0}'".format(url))
        jsonified = ujson.dumps(request)
        response = requests.post(url, data=jsonified, timeout=timeout)

    if response.ok:
        return ujson.loads(response.content)
    else:
        content = None
        if hasattr(response, 'content'):
            content = response.content
        elif hasattr(response, '_content'):
            content = response._content  # pylint: disable=W0212
        if content:
            if isinstance(content, bytes):
                http_error_msg = content.decode('ascii')
                try:
                    val = ujson.loads(http_error_msg)
                    http_error_msg = val
                except ValueError:
                    pass
                finally:
                    pass
            else:
                http_error_msg = ujson.loads(content)
            if isinstance(http_error_msg, dict):
                http_error_msg = "\n".join(
                    ["{0}: {1}".format(k, v) for k, v in sorted(http_error_msg.items())])
        else:
            http_error_msg = "ERROR"
        raise HTTPError(http_error_msg, response=response)
