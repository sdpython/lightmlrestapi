
.. _l-template-ml:

Templates
=========

Classes :class:`MLStorage <lightmlrestapi.mlapp.mlstorage.MLStorage>` and
:class:`MLStoragePost <lightmlrestapi.mlapp.mlstorage_rest.MLStoragePost>`
assume that a model is actionable by implementing
the following template:

.. runpython::

    from lightmlrestapi.testing.template_ml import __file__

    with open(__file__, "r", encoding="utf-8") as f:
        print(f.read())

The second template shows how to deal with images
with a dummy example which computes the distance
between two images.

.. runpython::

    from lightmlrestapi.testing.template_dl_light import __file__

    with open(__file__, "r", encoding="utf-8") as f:
        print(f.read())
