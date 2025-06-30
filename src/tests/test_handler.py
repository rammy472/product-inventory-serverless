import json
import pytest
from inventory import handler

@pytest.fixture
def context():
    return {}

def test_invalid_request(mocker):
    event = {"httpMethod": "PATCH", "path": "/products"}
    resp = handler.lambda_handler(event, {})
    assert resp["statusCode"] == 400

def test_create_and_get(mocker):
    mock_table = mocker.patch("inventory.handler.table")
    mock_table.put_item.return_value = {}
    event = {"httpMethod": "POST", "path": "/products", "body": json.dumps({"name": "Desk", "price": 30})}
    resp = handler.lambda_handler(event, {})
    assert resp["statusCode"] == 201