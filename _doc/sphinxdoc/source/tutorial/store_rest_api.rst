
.. l-store_rest_api:

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

    start_mlreststor --location=. --users=encrypted_passwords.txt

.. faqref::
    :title: Why the REST application does not log anything on screen?

    On Windows, logs disapper if the application is run with ``pythonw.exe``
    with command line::

        python -m lightmlrestapi start_mlreststor --location=. --users=encrypted_passwords.txt

    To restore the logging, option ``-u`` can be added:

        python -u -m lightmlrestapi start_mlreststor --location=. --users=encrypted_passwords.txt

Upload a machine learned model
==============================
