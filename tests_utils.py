from typing import List
import urllib.parse as urlparse
from urllib.parse import urlencode


def build_request_url(url, params):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urlencode(query)

    return urlparse.urlunparse(url_parts)


def assert_response_types(response):
    for idx in range(len(response["data"])):
        idx = str(idx)
        assert isinstance(response["data"][idx]["Pokemon"], str)
        assert isinstance(response["data"][idx]["Types"], list)
        assert isinstance(response["data"][idx]["HP"], int)
        assert isinstance(response["data"][idx]["Attack"], int)
        assert isinstance(response["data"][idx]["Special Attack"], int)
        assert isinstance(response["data"][idx]["Defense"], int)
        assert isinstance(response["data"][idx]["Special Defense"], int)
        