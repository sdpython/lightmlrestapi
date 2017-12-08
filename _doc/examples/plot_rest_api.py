"""
Starts and queries a REST API
=============================

This example starts a :epkg:`waitress` server, creates
a :epkg:`WSGI` application based on :epkg:`falcon`
and queries the REST API. This application
returns the prediction from a model trained
on :epkg:`Iris dataset`.
"""
####################
# Settings.
host = '127.0.0.1'
port = 8081

########################
# Creates a dummy application and starts a server in a different process.
# See :func:`dummy_application <lightmlrestapi.testing.dummy_applications.dummy_application>`.


def process_server(host, port):
    import logging
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.INFO)

    from lightmlrestapi.testing import dummy_application
    app = dummy_application()

    from waitress import serve
    serve(app, host=host, port=port)

##########################
# Saves this code into a file and we start it
# from a different process.


import os
import lightmlrestapi

header = """
import sys
sys.path.append(r'{0}')
""".format(os.path.join(os.path.dirname(lightmlrestapi.__file__), '..'))

import inspect
code = "".join(inspect.getsourcelines(process_server)[0])
code = header + code + "\nprocess_server('{0}', {1})\n".format(host, port)
dest = os.path.abspath('temp_scripts')
if not os.path.exists(dest):
    os.mkdir(dest)
code_file = os.path.join(dest, "_start_server.py")
with open(code_file, "w") as f:
    f.write(code)

import sys
from subprocess import Popen, PIPE
if sys.platform.startswith('win'):
    cmd = '{0} -u "{1}"'.format(sys.executable, code_file)
    proc = Popen(cmd)
else:
    cmd = [sys.executable, '-u', code_file]
    proc = Popen(cmd)
print('Start server, process id', proc.pid)

##########################
# Let's wait.
from time import sleep
sleep(3)

####################
# Let's query the server.

import requests
import ujson
features = ujson.dumps({'X': [0.1, 0.2]})
r = requests.post('http://127.0.0.1:8081', data=features)
print(r.json())

####################
# Let's stop the server.
from pyquickhelper.loghelper import reap_children
reap_children(subset={proc.pid}, fLOG=print)
