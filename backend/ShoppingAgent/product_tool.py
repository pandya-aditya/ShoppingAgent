# product_tool.py

from google.adk import tool

# Load dataset once



@tool
def search_products(query: str) -> dict:
    """
    Search products based on user query.
    Returns matching products (name, description, price, image).
    """
    results = []

    query_lower = query.lower()

    for item in PRODUCT_DATA:
        if (
            query_lower in item["name"].lower()
            or query_lower in item["description"].lower()
        ):
            results.append(item)

    return {"results": results}


@tool
def filter_by_price(max_price: float) -> dict:
    """Return products costing <= max_price."""
    results = [item for item in PRODUCT_DATA if item["price"] <= max_price]
    return {"results": results}
