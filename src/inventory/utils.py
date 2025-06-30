def validate_product(data):
    # Basic validation: name required, price must be positive number
    if "name" not in data or not data["name"]:
        return False, "Product 'name' is required"
    if "price" not in data or not isinstance(data["price"], (int, float)) or data["price"] < 0:
        return False, "Product 'price' must be a positive number"
    return True, ""