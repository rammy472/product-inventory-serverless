import json
import os
import uuid
import boto3
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.metrics import MetricUnit

logger = Logger()
tracer = Tracer()
metrics = Metrics(namespace="ProductInventory")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

@logger.inject_lambda_context
@tracer.capture_lambda_handler
@metrics.log_metrics
def lambda_handler(event, context):
    method = event["httpMethod"]
    path = event["path"]
    path_params = event.get("pathParameters") or {}
    body = json.loads(event.get("body", "{}")) if event.get("body") else {}

    if method == "POST" and path == "/products":
        # Create
        pid = str(uuid.uuid4())
        item = {"id": pid, **body}
        table.put_item(Item=item)
        metrics.add_metric(name="ProductsCreated", unit=MetricUnit.Count, value=1)
        return _resp(201, item)
    elif method == "GET" and path == "/products":
        # List all
        resp = table.scan()
        return _resp(200, resp.get("Items", []))
    elif method == "GET" and path_params.get("id"):
        # Get one
        pid = path_params["id"]
        resp = table.get_item(Key={"id": pid})
        if "Item" in resp:
            return _resp(200, resp["Item"])
        else:
            return _resp(404, {"error": "Product not found"})
    elif method == "PUT" and path_params.get("id"):
        # Update
        pid = path_params["id"]
        updates = ", ".join([f"#{k}=:{k}" for k in body])
        expr_attr_names = {f"#{k}": k for k in body}
        expr_attr_vals = {f":{k}": v for k, v in body.items()}
        table.update_item(
            Key={"id": pid},
            UpdateExpression=f"SET {updates}",
            ExpressionAttributeNames=expr_attr_names,
            ExpressionAttributeValues=expr_attr_vals
        )
        return _resp(200, {"message": "Product updated"})
    elif method == "DELETE" and path_params.get("id"):
        # Delete
        pid = path_params["id"]
        table.delete_item(Key={"id": pid})
        return _resp(204, None)
    else:
        return _resp(400, {"error": "Invalid request"})

def _resp(status, body):
    return {
        "statusCode": status,
        "body": json.dumps(body) if body is not None else "",
        "headers": {"Content-Type": "application/json"}
    }