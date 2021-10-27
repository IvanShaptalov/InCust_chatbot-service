import pytest

# from filters.filters import user_in_chat


@pytest.mark.config
def test_config_valid():
    try:
        from data import config
        print(config.CLIENT_BOT_TOKEN)
    except KeyError as e:
        assert False, "config valid failed"


@pytest.mark.internet
def test_internet_connection():
    import requests
    google = 'https://www.google.com/'
    try:
        requests.get(google)
    except Exception as e:
        print(e)
        assert False, 'check internet connection'
