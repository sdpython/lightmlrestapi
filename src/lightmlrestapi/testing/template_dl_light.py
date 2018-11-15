"""
@file
@brief Template application for a machine learning model
available through a REST API and using images like
deep learning models.
"""
import pickle
import numpy
import skimage.transform as skt


# Declare an id for the REST API.
def restapi_version():
    """
    Displays a version.
    """
    return "0.1.1235"


# Declare a loading function.
def restapi_load(model="dlimg.pkl"):
    """
    Loads the model.
    """
    with open(model, "rb") as f:
        loaded_model = pickle.load(f)
    return loaded_model


# Declare a predict function.
def restapi_predict(model, X):
    """
    Computes the prediction for model *clf*.

    :param clf: pipeline following :epkg:`scikit-learn` API
    :param X: image as a :epkg:`numpy` array
    :return: output of *predict_proba*
    """
    if not isinstance(X, numpy.ndarray):
        raise TypeError("X must be an array")
    im1 = model
    im2 = X
    im1 = skt.resize(im1, (3, 224, 224))
    im2 = skt.resize(im2, (3, 224, 224))
    diff = im1.ravel() - im2.ravel()
    total = numpy.abs(diff)
    return total.sum() / float(len(total)) / 255
