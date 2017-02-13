import flickr_api
import urllib2
from cStringIO import StringIO
import PIL.Image
from toolz import memoize

__all__ = ["search"]

# other licenses *might* be fine, these definitely are provided you attribute
USABLE_LICENSE_NAMES = {
    "Attribution License",
    "Attribution-NonCommercial License"
}


@memoize
def get_usable_license_ids():
    ids = []
    for flickr_license in flickr_api.License.getList():
        if flickr_license.name in USABLE_LICENSE_NAMES:
            ids.append(flickr_license.id)
    return ids


def search(keyword, keys):
    flickr_api.set_keys(keys["flickr_key"], keys["flickr_secret"])

    api_args = {
        "tags": keyword,
        "safe_search": 1,
        "media": "photos",
        "license": ",".join(get_usable_license_ids()),
        "sort": "relevance",
        "per_page": 1
    }

    response = flickr_api.Photo.search(**api_args)

    if not response:
        return None, None

    photo = response[0]

    reader = urllib2.urlopen(photo.getPhotoFile(size_label="Medium"))
    return photo, PIL.Image.open(StringIO(reader.read()))
