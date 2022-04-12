import responses
import requests

from decorator import decorator

GOOGLE_URL = "https://www.google.com/"
YOUTUBE_URL = "https://www.youtube.com/"


@responses.activate
@decorator
def mock_google(func, *args, **kwargs):
    responses.add(responses.GET, GOOGLE_URL, json={"success": True})
    return func(*args, **kwargs)


def business_logic():
    response = requests.get(GOOGLE_URL)
    payload = response.json()
    assert payload["success"]
    response = requests.get(YOUTUBE_URL)
    payload = response.json()
    assert payload["success"]


@mock_google
@responses.activate
def test_stuff():
    responses.add(
        responses.Response(method="GET", url=YOUTUBE_URL, json={"success": True})
    )
    business_logic()


@responses.activate
@mock_google
def test_stuff_in_a_different_order():
    responses.add(
        responses.Response(method="GET", url=YOUTUBE_URL, json={"success": True})
    )
    business_logic()
