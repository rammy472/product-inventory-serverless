from inventory.utils import validate_product

def test_validate_product():
    assert validate_product({"name": "Chair", "price": 10}) == (True, "")
    assert validate_product({"price": 10}) == (False, "Product 'name' is required")
    assert validate_product({"name": "Chair", "price": -2}) == (False, "Product 'price' must be a positive number")