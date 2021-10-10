from typing import List


def assert_response_types(response, idx):
    assert isinstance(response["data"][idx]["Pokemon"], str)
    assert isinstance(response["data"][idx]["Types"], list)
    assert isinstance(response["data"][idx]["HP"], int)
    assert isinstance(response["data"][idx]["Attack"], int)
    assert isinstance(response["data"][idx]["Special Attack"], int)
    assert isinstance(response["data"][idx]["Defense"], int)
    assert isinstance(response["data"][idx]["Special Defense"], int)