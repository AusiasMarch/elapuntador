import requests
from datetime import datetime

from core import config
from tests.utils.peso import create_random_item
from tests.utils.utils import get_server_api


def test_fetch_model(superuser_token_headers):
    server_api = get_server_api()
    data = {"version": "version_1"}
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/models/",
        headers=superuser_token_headers,
        params=data,
    )
    content = response.json()
    assert response.status_code == 200
    assert "version" in content
    assert "updated" in content
    assert "algorithm" in content
    assert "processed_version" in content


def test_fetch_model_info(superuser_token_headers):
    server_api = get_server_api()
    data = {"start": 0, "limit": 5}
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/models/info",
        headers=superuser_token_headers,
        params=data,
    )
    content = response.json()
    assert response.status_code == 200
    assert isinstance(content, list) and len(content) == 5
    for item in content:
        assert "version" in item
        assert "updated" in item
        assert "algorithm" in item
        assert "processed_version" in item


def test_fit_model(superuser_token_headers):
    server_api = get_server_api()
    data = {"version": "version_1", "processed_version": "version_1", "algorithm": "NN"}
    response = requests.post(
        f"{server_api}{config.API_V1_STR}/models/fit",
        headers=superuser_token_headers,
        json=data,
    )
    content = response.json()
    assert response.status_code == 202
    assert "email" in content
    assert content["version"] == data["version"]
    assert content["processed_version"] == data["processed_version"]
    assert content["algorithm"] == data["algorithm"]


def test_test_model(superuser_token_headers):
    server_api = get_server_api()
    data = {
        "version": "version_1",
        "processed_version": "version_1",
        "model_version": "version_1",
    }
    response = requests.post(
        f"{server_api}{config.API_V1_STR}/models/test",
        headers=superuser_token_headers,
        json=data,
    )
    content = response.json()
    assert response.status_code == 202
    assert "email" in content
    assert content["version"] == data["version"]
    assert content["processed_version"] == data["processed_version"]


def test_predict_model(superuser_token_headers):
    server_api = get_server_api()
    data = {
        "version": "version_1",
        "processed_version": "version_1",
        "model_version": "version_1",
    }
    response = requests.post(
        f"{server_api}{config.API_V1_STR}/models/predict",
        headers=superuser_token_headers,
        json=data,
    )
    content = response.json()
    assert response.status_code == 202
    assert "email" in content
    assert content["version"] == data["version"]
    assert content["processed_version"] == data["processed_version"]


def test_get_result(superuser_token_headers):
    server_api = get_server_api()
    data = {"version": "version_1"}
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/models/result",
        headers=superuser_token_headers,
        params=data,
    )
    content = response.json()
    assert response.status_code == 200
    assert "version" in content
    assert "updated" in content
    assert "model_version" in content
    assert "processed_version" in content


def test_get_result_info(superuser_token_headers):
    server_api = get_server_api()
    data = {"start": 0, "limit": 5}
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/models/result/info",
        headers=superuser_token_headers,
        params=data,
    )
    content = response.json()
    assert response.status_code == 200
    assert isinstance(content, list) and len(content) == 5
    for item in content:
        assert "version" in item
        assert "updated" in item
        assert "model_version" in item
        assert "processed_version" in item


def test_get_prediction(superuser_token_headers):
    server_api = get_server_api()
    data = {"version": "version_1"}
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/models/prediction",
        headers=superuser_token_headers,
        params=data,
    )
    content = response.json()
    assert response.status_code == 200
    assert "version" in content
    assert "updated" in content
    assert "model_version" in content
    assert "processed_version" in content


def test_get_prediction_info(superuser_token_headers):
    server_api = get_server_api()
    data = {"start": 0, "limit": 5}
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/models/prediction/info",
        headers=superuser_token_headers,
        params=data,
    )
    content = response.json()
    assert response.status_code == 200
    assert isinstance(content, list) and len(content) == 5
    for item in content:
        assert "version" in item
        assert "updated" in item
        assert "model_version" in item
        assert "processed_version" in item
