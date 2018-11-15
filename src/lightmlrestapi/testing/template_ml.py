"""
@file
@brief Template application for a machine learning model
available through a REST API.
"""
import pickle


# Declare an id for the REST API.
def restapi_version():
    """
    Displays a version.
    """
    return "0.1.1234"


# Declare a loading function.
def restapi_load(model="iris2.pkl"):
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

    :param model: pipeline following :epkg:`scikit-learn` API
    :param X: inputs
    :return: output of *predict_proba*
    """
    return model.predict_proba(X)
