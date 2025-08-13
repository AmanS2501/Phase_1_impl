import requests

ALLMART_API_URL = "https://api.allmart.fashion/api/v1/products"

def search_products(filters, page=1, limit=12):
    params = {
        "page": page,
        "limit": limit,
        "sortBy": "averageRating",
        "sortOrder": "desc",
        "inStock": "true"
    }
    category = filters.get("category")
    if category and category.lower() != "all":
        params["categorySlug"] = category
    if "min_price" in filters:
        params["minPrice"] = filters["min_price"]
    if "max_price" in filters:
        params["maxPrice"] = filters["max_price"]
    try:
        resp = requests.get(ALLMART_API_URL, params=params, timeout=10)
        data = resp.json()
    except Exception as e:
        return {"error": str(e)}
    products = (
        data.get("data", {}).get("data")
        or data.get("data", [])
        or data.get("products", [])
        or []
    )
    products = [p for p in products if isinstance(p, dict)]
    return products
