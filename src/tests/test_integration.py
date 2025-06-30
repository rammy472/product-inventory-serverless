import os
import json
import boto3
import pytest
from moto import mock_dynamodb
from inventory import handler

@pytest.fixture(autouse=True)
def setup_table(monkeypatch):
    with mock_dynamodb():
        client = boto3.resource("dynamodb", region_name="us-east-1")
        table = client.create_table(
            TableName="ProductTable",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST"
        )
        monkeypatch.setenv("TABLE_NAME", "ProductTable")
        yield

def test_add_and_list():
    # Add a product
    event = {"httpMethod": "POST", "path": "/products", "body": json.dumps({"name": "Lamp", "price": 15})}
    resp = handler.lambda_handler(event, {})
    assert resp["statusCode"] == 201
    item = json.loads(resp["body"])
    # List products
    event = {"httpMethod": "GET", "path": "/products"}
    resp = handler.lambda_handler(event, {})
    assert resp["statusCode"] == 200
    list_body = json.loads(resp["body"])
    assert any(p["id"] == item["id"] for p in list_body)