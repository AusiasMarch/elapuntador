import requests
from datetime import datetime

from core import config
from tests.utils.peso import create_random_item
from tests.utils.utils import get_server_api


def test_fetch_raw(superuser_token_headers):
    server_api = get_server_api()
    data = {"date_from": "2010-04-17", "date_to": "2011-04-17"}
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/data/raw-data/",
        headers=superuser_token_headers,
        params=data,
    )
    content = response.json()
    assert response.status_code == 202
    assert "updated" in content
    assert datetime.strptime(
        content["date_from"], "%Y-%m-%dT%H:%M:%S"
    ) == datetime.strptime(data["date_from"], "%Y-%m-%d")
    assert datetime.strptime(
        content["date_to"], "%Y-%m-%dT%H:%M:%S"
    ) == datetime.strptime(data["date_to"], "%Y-%m-%d")
    assert "email" in content


def test_refresh_raw(superuser_token_headers):
    server_api = get_server_api()
    response = requests.post(
        f"{server_api}{config.API_V1_STR}/data/raw-data/",
        headers=superuser_token_headers,
    )
    content = response.json()
    assert response.status_code == 202
    assert "updated" in content
    assert "email" in content


def test_info_raw(superuser_token_headers):
    server_api = get_server_api()
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/data/raw-data/info",
        headers=superuser_token_headers,
    )
    content = response.json()
    assert response.status_code == 200
    assert "updated" in content
    assert "date_from" in content
    assert "date_to" in content


def test_fetch_processed(superuser_token_headers):
    server_api = get_server_api()
    data = {"version": "version_1", "date_from": "2014-05-18", "date_to": "2015-05-26"}
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/data/processed-data/",
        headers=superuser_token_headers,
        params=data,
    )
    content = response.json()
    assert response.status_code == 200
    assert "updated" in content
    assert content["version"] == data["version"]
    assert datetime.strptime(
        content["date_from"], "%Y-%m-%dT%H:%M:%S"
    ) == datetime.strptime(data["date_from"], "%Y-%m-%d")
    assert datetime.strptime(
        content["date_to"], "%Y-%m-%dT%H:%M:%S"
    ) == datetime.strptime(data["date_to"], "%Y-%m-%d")
    assert "sampling" in content
    try:
        int(content["sampling"])
    except ValueError:
        raise AssertionError("sampling is not an int")
    assert "split" in content
    try:
        int(content["split"])
    except ValueError:
        raise AssertionError("split is not an int")
    assert "transformations" in content and isinstance(content["transformations"], list)


def test_refresh_processed(superuser_token_headers):
    server_api = get_server_api()
    data = {
        "version": "version 1",
        "date_from": "2018-05-26",
        "date_to": "2019-12-28",
        "sampling": 20,
        "split": 80,
    }
    response = requests.post(
        f"{server_api}{config.API_V1_STR}/data/processed-data/",
        headers=superuser_token_headers,
        json=data,
    )
    content = response.json()
    assert response.status_code == 202
    assert "updated" in content
    assert content["version"] == data["version"]
    assert datetime.strptime(
        content["date_from"], "%Y-%m-%dT%H:%M:%S"
    ) == datetime.strptime(data["date_from"], "%Y-%m-%d")
    assert datetime.strptime(
        content["date_to"], "%Y-%m-%dT%H:%M:%S"
    ) == datetime.strptime(data["date_to"], "%Y-%m-%d")
    try:
        content["sampling"] = int(content["sampling"])
    except ValueError:
        raise AssertionError("sampling is not an int")
    assert content["sampling"] == data["sampling"]
    try:
        content["split"] = int(content["split"])
    except ValueError:
        raise AssertionError("split is not an int")
    assert content["split"] == data["split"]
    assert isinstance(content["transformations"], list)
    assert "email" in content


def test_info_processed(superuser_token_headers):
    server_api = get_server_api()
    data = {"start": 0, "limit": 5}
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/data/processed-data/info",
        headers=superuser_token_headers,
        params=data,
    )
    content = response.json()
    assert response.status_code == 200
    assert isinstance(content, list) and len(content) == 5
    for item in content:
        assert "updated" in item
        assert "version" in item
        assert "date_from" in item
        assert "date_to" in item
        assert "sampling" in item
        assert "split" in item
        assert isinstance(item["transformations"], list)
