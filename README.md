# Serverless Product Inventory

A fully serverless product inventory API using AWS Lambda, DynamoDB, API Gateway, AWS SAM, and Lambda Powertools.  
Includes unit and integration tests, and follows best practices for observability and Infrastructure as Code.

## Features

- Add a product: `POST /products`
- List all products: `GET /products`
- Get product by ID: `GET /products/{id}`
- Update a product: `PUT /products/{id}`
- Delete a product: `DELETE /products/{id}`

## Development Steps

1. **Infrastructure as Code:**  
   - All resources are defined in `template.yaml` using AWS SAM.
2. **Lambda Powertools:**  
   - Used for logging, tracing, and metrics in `handler.py`.
3. **Testing:**  
   - Unit tests (`test_utils.py`, `test_handler.py`)
   - Integration tests with DynamoDB mocked by `moto` (`test_integration.py`)
   - Run locally: `pytest src/tests/`
4. **Debugging:**  
   - Used rich logs with Powertools, API tested with `sam local start-api`.
   - Traces/metrics/logs available in CloudWatch when deployed.

## Local Development

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest src/tests/
sam local start-api
```

## Lessons Learned

- Lambda Powertools makes observability easy.
- moto is essential for quick and reliable integration testing.
- IaC (SAM) is invaluable for consistent, repeatable environments.
