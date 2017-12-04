"""
@file
@brief Playground with images.
"""
import io
import os
import base64
import numpy
from PIL import Image


def image2array(img):
    """
    Converts a color imaged into an array.

    @param      img     :epkg:`PIL:Image.Image`
    @return             :epkg:`numpy:array`
    """
    im_arr = numpy.fromstring(img.tobytes(), dtype=numpy.uint8)
    im_arr = im_arr.reshape((img.size[1], img.size[0], 3))
    return im_arr


def image2base64(path):
    """
    Encodes an image into :epkg:`*py:base64`.

    @param      path        filename
    @return                 format, base64

    The format is the file extension.
    """
    ext = os.path.splitext(path)[-1].lower().strip('.')
    with open(path, "rb") as f:
        content = f.read()
    return 'image/' + ext, base64.b64encode(content)


def base642image(encoded):
    """
    Gets an encoded image and builds an
    :epkg:`PIL:Image.Image` from it.

    @param      encoded     :epkg:`*py:base64` encoded image
                            (see @see fn image2base64)
    @return                 :epkg:`PIL:Image.Image`
    """
    cont = base64.b64decode(encoded)
    return Image.open(io.BytesIO(cont))
