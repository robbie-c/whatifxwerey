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


def what_if_x_were_y(x_phrase, y_phrase, keys, search_source=DEFAULT_SEARCH_SOURCE):
    if search_source == SearchSources.google:
        search = google_custom_search.search
    else:
        search = flickr.search
    x_meta, x_image = search(x_phrase, keys=keys)
    y_meta, y_image = search(y_phrase, keys=keys)

    y_image = image_max_size(y_image)

    return merge(x_image, y_image)


def image_max_size(image, max_size=512):
    ratio = max_size / max(*image.size)

    if ratio >= 1:
        return image

    new_width = int(image.size[0] * ratio)
    new_height = int(image.size[1] * ratio)

    return image.resize((new_width, new_height), resample=PIL.Image.LANCZOS)


def main():
    import argparse
    import json
    parser = argparse.ArgumentParser(description='What if X were Y? Find out using image search APIs and deepdream')
    parser.add_argument('x_phrase', type=str, help='the search phrase for X')
    parser.add_argument('y_phrase', type=str, help='the search phrase for Y')
    parser.add_argument('keyfile_json_path', type=str, help='a JSON file containing keys for image searches')
    parser.add_argument('output_path', type=str, help='where to save the resulting jpeg')
    args = parser.parse_args()
    with open(args.keyfile_json_path) as data_file:
        keys = json.load(data_file)
    output_image = what_if_x_were_y(args.x_phrase, args.y_phrase, keys)
    output_image.save(args.output_path, "jpeg")


if __name__ == "__main__":
    main()
