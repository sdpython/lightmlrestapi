"""
@file
@brief Creates and runs an Falcon application.
"""
import os
import sys
import logging
from pyquickhelper.cli.cli_helper import call_cli_function


def start_mlrestapi(name='dummy', host='127.0.0.1', port=8081, nostart=False, wsgi='waitress',
                    fLOG=print):
    """
    Creates an :epkg:`falcon` application and
    runs it through a :epkg:`wsgi` server.

    :param name: class name or filename which defines the application
    :param host: host
    :param port: port
    :param nostart: do not start the wsgi server
    :param wsgi: wsgi framework which runs the falcon application
    :param fLOG: logging function

    Only :epkg:`waitress` is implemented right now.
    Other option such as :epkg:`mod_wsgi` with :epkg:`Apache`.
    :epkg:`uwsgi` could be also be implemented.
    could be added in the future. The command line
    can be tested with a dummy application (``app_name='dummy'``).
    """
    try:
        from ..mlpost import MachineLearningPost
    except (ImportError, ValueError):
        folder = os.path.normpath(os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", ".."))
        sys.path.append(folder)
        from lightmlrestapi.mlpost import MachineLearningPost

    if name == "dummy":
        app = MachineLearningPost.dummy_application()
    elif '.py' in name:
        raise NotImplementedError(
            "Unable to get application from filename '{}'. Not implemented.".format(name))
    else:
        raise NotImplementedError(
            "Application '{}' is not implemented.".format(name))

    if wsgi == 'waitress':
        from waitress import serve
        if not nostart:
            fLOG("[start_mlrestapi] serve(app, host='{}', port='{}')".format(host, port))
            logger = logging.getLogger('waitress')
            logger.setLevel(logging.INFO)
            serve(app, host=host, port=port)
        else:
            fLOG("[start_mlrestapi] do not run serve(app, host='{}', port='{}')".format(
                host, port))
    else:
        raise NotImplementedError(
            "Server '{}' is not implemented.".format(wsgi))

    return app


def _start_mlrestapi(fLOG=print, args=None):
    """
    Creates an falcon application and starts it through a wsgi application.

    @param      fLOG        logging function
    @param      args        to overwrite ``sys.args``

    .. cmdref::
        :title: Creates an falcon application and starts it through a wsgi application
        :cmd: lightmlrestapi.cli.make_ml_app:start_mlrestapi
        :lid: cmd_start_mlrestapi_cmd

        Creates an :epkg:`falcon` application and starts it through a :epkg:`wsgi` server.
    """
    epkg_dictionary = dict(falcon='https://falconframework.org/',
                           Apache='https://httpd.apache.org/',
                           mod_wsgi='https://modwsgi.readthedocs.io/en/develop/',
                           uwsgi='https://uwsgi-docs.readthedocs.io/en/latest/',
                           wsgi='https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface',
                           waitress='https://docs.pylonsproject.org/projects/waitress/en/latest/')
    call_cli_function(start_mlrestapi, args=args, fLOG=fLOG, skip_parameters=('fLOG',),
                      epkg_dictionary=epkg_dictionary)


if __name__ == "__main__":
    _start_mlrestapi()
