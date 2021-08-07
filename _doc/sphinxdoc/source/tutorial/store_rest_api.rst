
.. _l-store_rest_api:

===============================================
REST API to a storage for machine learned model
===============================================

This page shows how to set up an application available
through a REST API which stores and runs machine learned
models. This was developped for a hackathon to be able
to compare multiple models in the same conditions.

.. contents::
    :local:

Every command line used below show can be run
prefixed by ``python -m lightmlrestapi <command line>``
once the model *lightmlrestapi* is installed.

Train a model on Iris
=====================

We first need a machine learning model to test the whole
process of publishing the model the web application and
then call it to predict. We use the
:epkg:`iris` dataset. The important part consists in saving
the model with :epkg:`pickle`.

.. runpython::
    :showcode:
    :warningout: UserWarning, FutureWarning

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
    model_file = "model_iris.pkl"
    with open(model_file, "wb") as f:
        f.write(model_data)

Second step is to write the script which loads
the model and then predict with a specific API.
If the model follows :epkg:`scikit-learn`, the
following code should work just by replacing the
model name.

.. runpython::
    :showcode:
    :warningout: UserWarning, FutureWarning

    from lightmlrestapi.testing import template_ml
    with open(template_ml.__file__, "r", encoding="utf-8") as f:
        code = f.read()
    code = code.replace("iris2.pkl", "model_iris.plk")
    with open("model_iris.py", "w", encoding="utf-8") as f:
        f.write(code)
    print(code)

The step created two files ``model_iris.pkl`` and ``model_iris.py``.
Let's now switch to the REST API application.

Set up authenticated users
==========================

Only the participants are allowed to store and
test their models. We create a file with
a list of login and password in a file with
two columns and no header encoding with
:epkg:`utf-8`.

::

    xavier,passWrd!
    clémence,notmybirthday

Let's encrypt the following file.

::

    encrypt_pwd --input=users.txt --output=encrypted_passwords.txt

It shows:

::

    [encrypt_pwd] encrypt 'users.txt'
    [encrypt_pwd] to      'encrypted_passwords.txt'
    [encrypt_pwd] done.

File ``'encrypted_passwords.txt'`` contains the following:

::

    xavier,0cb3b6f95cbb4462d34d21c4fd6fc8b9425ddac9d9c12e1940bb2e4f
    clémence,0cc9be13cb6bbbdac48e3b30c306846405388fd4f4bd0a545cb004ad

Start the REST API
==================

The REST API can be started from the folder used to store
machine learned models as follows:

::

    start_mlreststor --location=. --users=encrypted_passwords.txt --host=127.0.0.1 --port=8095

.. faqref::
    :title: Why the REST application does not log anything on screen?

    On Windows, logs disapper if the application is run with ``pythonw.exe``
    with command line::

        python -m lightmlrestapi start_mlreststor --location=. --users=encrypted_passwords.txt

    To restore the logging, option ``-u`` can be added:

        python -u -m lightmlrestapi start_mlreststor --location=. --users=encrypted_passwords.txt

The web application cannot delete machine learned models or
overwrite one. It can be stopped and restarted without losing
models as they stored on disk.

Upload a machine learned model
==============================

We upload the two files as mentioned created in the first step.
The name can only contains lower letters and digits
except in the first position. The model is now uploaded.

::

    upload_model --name=xavier/iris1 --url=http://127.0.0.1:8095/ --pyfile=model_iris.py --data=model_iris.pkl --login=xavier --pwd=passWrd!

The following code can be replaced by a :epkg:`python`
maybe easier to automated from a notebook.

::

    from lightmlrestapi.netrest import submit_rest_request, json_upload_model
    req = json_upload_model(name="xavier/iris1", pyfile="model_iris.py", data="model_iris.pkl")
    submit_rest_request(req, login="xavier", pwd="passWrd!",
                        url="http://127.0.0.1:8095/", fLOG=print)

Compute prediction through the REST API
=======================================

The following piece of code calls the service and the prediction
for many obersvation in one row.

::

    from lightmlrestapi.netrest import json_predict_model, submit_rest_request
    from sklearn import datasets

    iris = datasets.load_iris()
    X = iris.data[:, :2]

    req = json_predict_model("xavier/iris1", X)
    res = submit_rest_request(req, login="xavier", pwd="passWrd!",
                              url="http://127.0.0.1:8095/", fLOG=print)
    print(res)

::

    {'output': [[0.8180557319, 0.1140978624, 0.06784640580000001],
                [0.6427973036, 0.22443658900000002, 0.1327661074],
     ...

Example with Keras
==================

Let's retrieve and save a model trained
on :epkg:`ImageNet`.

.. runpython::
    :showcode:
    :warningout: UserWarning, FutureWarning

    try:
        import keras
        from keras.applications.mobilenet import MobileNet
        model = MobileNet(input_shape=None, alpha=1.0, depth_multiplier=1,
                          dropout=1e-3, include_top=True,
                          weights='imagenet', input_tensor=None,
                          pooling=None, classes=1000)
        model_name = "mobile.keras"
        model.save(model_name)
    except ImportError:
        print("Keras is not installed.")
    except AttributeError as e:
        print(e)

Then we create the :epkg:`python` application.

.. runpython::
    :showcode:
    :warningout: UserWarning, FutureWarning

    from lightmlrestapi.testing import template_dl_keras
    with open(template_dl_keras.__file__, "r", encoding="utf-8") as f:
        code = f.read()
    code = code.replace("dlmodel.keras", "mobile.keras")
    with open("model_keras.py", "w", encoding="utf-8") as f:
        f.write(code)
    print(code)

Next we upload the model to the wep application:

::

    from lightmlrestapi.netrest import submit_rest_request, json_upload_model
    req = json_upload_model(name="xavier/keras1", pyfile="model_keras.py", data="mobile.keras")
    submit_rest_request(req, login="xavier", pwd="passWrd!",
                        url="http://127.0.0.1:8095/", fLOG=print)

Finally let's predict:

::

    from lightmlrestapi.netrest import json_predict_model, submit_rest_request
    from lightmlrestapi.args import image2base64
    from lightmlrestapi.testing.data import get_wiki_img
    import numpy
    from PIL import Image
    import base64
    import pickle

    img = "custom_immage.png" # or get_wiki_img() for a dummy one
    arr = numpy.array(Image.open(img))
    img_b64 = base64.b64encode(pickle.dumps(arr))

    req = json_predict_model("xavier/keras2", img_b64, format='img')
    res = submit_rest_request(req, login="xavier", pwd="passWrd!",
                              url="http://127.0.0.1:8092/", fLOG=print)
    print(res)

That produces:

::

    {'output': [[3.997e-07, 3.28143e-05, 8.70764e-05, ...

Example with Torch
==================

Let's retrieve and save a model trained
on :epkg:`ImageNet`.

.. runpython::
    :showcode:
    :warningout: UserWarning, FutureWarning

    try:
        import torchvision.models as models  # pylint: disable=E0401
        import torch
        model = models.squeezenet1_0(pretrained=True)
        model_name = "model.torch"
        torch.save(model, model_name)
    except ImportError:
        print("Keras is not installed.")
    except AttributeError as e:
        print(e)

Then we create the :epkg:`python` application.

.. runpython::
    :showcode:
    :warningout: UserWarning, FutureWarning

    from lightmlrestapi.testing import template_dl_torch
    with open(template_dl_torch.__file__, "r", encoding="utf-8") as f:
        code = f.read()
    code = code.replace("dlmodel.torch", "squeeze.torch")
    with open("model_torch.py", "w", encoding="utf-8") as f:
        f.write(code)
    print(code)

Next we upload the model to the wep application:

::

    from lightmlrestapi.netrest import submit_rest_request, json_upload_model
    req = json_upload_model(name="xavier/keras1", pyfile="model_keras.py", data="mobile.keras")
    submit_rest_request(req, login="xavier", pwd="passWrd!",
                        url="http://127.0.0.1:8093/", fLOG=print)

Finally let's predict:

::

    from lightmlrestapi.netrest import json_predict_model, submit_rest_request
    from lightmlrestapi.args import image2base64
    from lightmlrestapi.testing.data import get_wiki_img
    import numpy
    from PIL import Image
    import base64
    import pickle

    img = "custom_immage.png" # or get_wiki_img() for a dummy one
    arr = numpy.array(Image.open(img))
    img_b64 = base64.b64encode(pickle.dumps(arr))

    req = json_predict_model("xavier/torch1", img_b64, format='img')
    res = submit_rest_request(req, login="xavier", pwd="passWrd!",
                              url="http://127.0.0.1:8093/", fLOG=print)
    print(res)

That produces:

::

    {'output': [[1.3296715021, 3.0834584235999998, 0.5387064219000001, ...
