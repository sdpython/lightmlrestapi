# -*- coding: utf-8 -*-
"""
Publishes and queries a mchaine learned model through a REST API
================================================================

This example starts a :epkg:`waitress` server, creates
a :epkg:`WSGI` application based on :epkg:`falcon`
and queries the REST API. This application
returns the prediction from a model trained
on :epkg:`Iris dataset`.
"""
####################
# Settings.
import os
host = '127.0.0.1'
port = 8093
location = os.path.abspath('temp_scripts_ml').replace("\\", "/")

########################
# We need users and to encrypt
# passwords.

users = """xavier,passWrd!
clémence,notmybirthday"""
with open("users.txt", "w", encoding="utf-8") as f:
    f.write(users)

from lightmlrestapi.cli import encrypt_pwd
if not os.path.exists(location):
    os.mkdir(location)
encrypt_pwd("users.txt", os.path.join(location, "encrypted_users.txt"))

########################
# Let's train a machine learned model and pickle the model.
from sklearn import datasets
from sklearn.linear_model import LogisticRegression

iris = datasets.load_iris()
X = iris.data[:, :2]  # we only take the first two features.
y = iris.target
clf = LogisticRegression()
clf.fit(X, y)

# save with pickle
import pickle
model_data = pickle.dumps(clf)
model_file = "model_iris2.pkl"
with open(model_file, "wb") as f:
    f.write(model_data)

###########################
# We create a file which follows the API defined
# in tutoral :ref:`l-store_rest_api`.

from lightmlrestapi.testing import template_ml
with open(template_ml.__file__, "r", encoding="utf-8") as f:
    code = f.read()
code = code.replace("iris2.pkl", model_file)
with open("model_iris.py", "w", encoding="utf-8") as f:
    f.write(code)
print(code)

########################
# Creates a dummy application and starts a server in a different process.
# See :func:`dummy_application <lightmlrestapi.testing.dummy_applications.dummy_application>`.


def process_server(host, port, location):
    from lightmlrestapi.cli import start_mlreststor
    import os
    with open("log.log", "a", encoding="utf-8") as f:
        def flog(*li):
            f.write(" ".join(str(_) for _ in li) + "\n")
            f.flush()
        flog("create app in ", os.getcwd())
        app = start_mlreststor(location=location, name='ml',
                               nostart=True, wsgi=None,
                               secret='', users='encrypted_users.txt',
                               fLOG=flog)
        from waitress import serve
        serve(app, host=host, port=port, url_scheme='https')


##########################
# Saves this code into a file and we start it
# from a different process.
import lightmlrestapi

header = """
import sys
sys.path.append(r'{0}')
""".format(os.path.join(os.path.dirname(lightmlrestapi.__file__), '..'))

import inspect
code = "".join(inspect.getsourcelines(process_server)[0])
code = header + code + \
    "\nprocess_server('{0}', {1}, '{2}')\n".format(host, port, location)
if not os.path.exists(location):
    os.mkdir(location)
code_file = os.path.join(location, "_start_server_store.py")
print("Write file '{0}'.".format(code_file))
with open(code_file, "w") as f:
    f.write(code)

import sys
import os
from subprocess import Popen
if sys.platform.startswith('win'):
    cmd = '{0} -u "{1}"'.format(sys.executable, code_file)
    print("Running '{0}'".format(cmd))
    proc = Popen(cmd, cwd=location)
else:
    cmd = [sys.executable, '-u', code_file]
    print("Running '{0}'".format(cmd))
    proc = Popen(cmd, cwd=location)
print('Start server, process id', proc.pid)

##########################
# Let's wait.
from time import sleep
sleep(5)

####################
# Let's publish the machine learned model.
import random
url = 'http://{0}:{1}/'.format(host, port)
model_name = "xavier/iris%d" % random.randint(0, 1000)

from lightmlrestapi.netrest import submit_rest_request, json_upload_model
req = json_upload_model(name=model_name,
                        pyfile="model_iris.py", data=model_file)
r = submit_rest_request(req, login="xavier", timeout=600,
                        pwd="passWrd!", url=url, fLOG=print)
print(r)

####################
# Let's query the machine learned model.
from lightmlrestapi.netrest import json_predict_model, submit_rest_request
from sklearn import datasets

iris = datasets.load_iris()
X = iris.data[:, :2]

req = json_predict_model(model_name, X)
res = submit_rest_request(
    req, login="xavier", pwd="passWrd!", url=url, fLOG=print)
print(res)

####################
# Let's measure the processing time.


def query_model(X):
    req = json_predict_model(model_name, X)
    return submit_rest_request(req, login="xavier", pwd="passWrd!", url=url, fLOG=None)


import timeit
N = 100
print(timeit.timeit('query_model(X)', number=N, globals=globals()) / N)

####################
# Let's stop the server.
from pyquickhelper.loghelper import reap_children
reap_children(subset={proc.pid}, fLOG=print)
