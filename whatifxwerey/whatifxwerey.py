from __future__ import division
from . import flickr
from . import google_custom_search
from .deepdream import merge
from enum import Enum
import PIL.Image

__all__ = ["SearchSources", "DEFAULT_SEARCH_SOURCE", "what_if_x_were_y"]


class SearchSources(Enum):
    flickr = 1
    google = 2

DEFAULT_SEARCH_SOURCE = SearchSources.google


def what_if_x_were_y(x_phrase, y_phrase, search_source=DEFAULT_SEARCH_SOURCE, keys=None):
    if search_source == SearchSources.google:
        search = google_custom_search.search
    else:
        search = flickr.search
    x_meta, x_image = search(x_phrase, keys=keys)
    y_meta, y_image = search(y_phrase, keys=keys)

    y_image = image_max_size(y_image)

    return merge(x_image, y_image)


def image_max_size(image, maxSize=512):
    ratio = maxSize / max(*image.size)

    if ratio >= 1:
        return image

    new_width = int(image.size[0] * ratio)
    new_height = int(image.size[1] * ratio)

    return image.resize((new_width, new_height), resample=PIL.Image.LANCZOS)


orangeImage = imageMaxSize(orangeImage)

bananaImage.save("banana.jpg", "jpeg")
orangeImage.save("orange.jpg", "jpeg")

merge(bananaImage, orangeImage)
