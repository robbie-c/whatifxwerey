import urllib
import urllib2
import PIL.Image
from cStringIO import StringIO

import requests

SEARCH_URL = "https://www.googleapis.com/customsearch/v1"


def request_string(query, keys):
    params = {
        "q": query,
        "cx": keys.google_custom_search_id,
        "key": keys.google_custom_search_key,
        "fileType": "jpg",
        "filter": "1",
        "imgColorType": "color",
        "imgType": "photo",
        "lr": "lang_en",
        "num": 1,
        "safe": "high",
        "searchType": "image"
    }

    return SEARCH_URL + "?" + urllib.urlencode(params)


def search(keyword, keys=None):

    search_response = requests.get(request_string(keyword, keys)).json()

    if not search_response["items"]:
        return None, None

    photo = search_response["items"][0]

    reader = urllib2.urlopen(photo["link"])
    return photo, PIL.Image.open(StringIO(reader.read()))
