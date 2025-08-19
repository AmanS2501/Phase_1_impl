from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from typing import Optional, List
import os
import json
import requests

mcp = FastMCP(name="AllmartServer")

DATA_FOLDER = "data"

# Product model
class Product(BaseModel):
    id: str
    title: str
    price: Optional[float]
    brand: Optional[str] = None
    category: Optional[str] = None

class AddToCartInput(BaseModel):
    user_id: str
    product: Product

class RemoveFromCartInput(BaseModel):
    user_id: str
    product_id: str

class ShowCartInput(BaseModel):
    user_id: str

class SearchProductFilters(BaseModel):
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None

class SearchProductsInput(BaseModel):
    filters: SearchProductFilters
    page: Optional[int] = 1
    limit: Optional[int] = 12

class FAQInput(BaseModel):
    query: str

def get_cart_path(user_id: str) -> str:
    os.makedirs(DATA_FOLDER, exist_ok=True)
    return os.path.join(DATA_FOLDER, f"cart_{user_id}.json")

def load_cart(user_id: str) -> List[dict]:
    path = get_cart_path(user_id)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_cart(user_id: str, cart: List[dict]):
    path = get_cart_path(user_id)
    with open(path, "w") as f:
        json.dump(cart, f, indent=2)

@mcp.tool()
def show_cart(input: ShowCartInput) -> List[Product]:
    """Show items in the user's cart."""
    cart = load_cart(input.user_id)
    return cart

@mcp.tool()
def add_to_cart(input: AddToCartInput) -> str:
    """Add a product to user's cart."""
    cart = load_cart(input.user_id)
    if any(item['id'] == input.product.id for item in cart):
        return "Product already in cart."
    cart.append(input.product.dict())
    save_cart(input.user_id, cart)
    return "Product added to cart."

@mcp.tool()
def remove_from_cart(input: RemoveFromCartInput) -> str:
    """Remove a product from user's cart."""
    cart = load_cart(input.user_id)
    new_cart = [item for item in cart if item['id'] != input.product_id]
    if len(new_cart) == len(cart):
        return "Product not found in cart."
    save_cart(input.user_id, new_cart)
    return "Product removed from cart."

@mcp.tool()
def search_products(input: SearchProductsInput) -> List[Product]:
    """Search products using filters."""
    base_url = "https://api.allmart.fashion/api/v1/products"
    params = {
        "page": input.page or 1,
        "limit": input.limit or 12,
        "sortBy": "averageRating",
        "sortOrder": "desc",
        "inStock": "true"
    }
    filters = input.filters
    if filters.category and filters.category.lower() != "all":
        params["categorySlug"] = filters.category
    if filters.min_price is not None:
        params["minPrice"] = filters.min_price
    if filters.max_price is not None:
        params["maxPrice"] = filters.max_price
    try:
        resp = requests.get(base_url, params=params, timeout=10)
        data = resp.json()
        products_raw = (
            data.get("data", {}).get("data", [])
            or data.get("data", [])
            or data.get("products", [])
        )
        # Fix: Only return items that are dicts!
        products = [p for p in products_raw if isinstance(p, dict)]
        # Convert to Product models, or dicts for client
        return [Product(
            id=p.get("id"),
            title=p.get("title"),
            price=p.get("price"),
            brand=p.get("brand"),
            category=p.get("categoryId")
        ).dict() for p in products]
    except Exception as e:
        print(f"API/product error: {e}")
        return []


FAQ_DATA = {
    "return": "You can return any product within 7 days for a full refund.",
    "shipping": "We ship orders within 1-2 business days.",
    "payment": "We accept major credit cards, UPI, and net banking.",
    "warranty": "Most electronics have a 1-year warranty.",
}

@mcp.tool()
def faq(input: FAQInput) -> str:
    """Answer frequently asked questions."""
    q = input.query.lower()
    for key, ans in FAQ_DATA.items():
        if key in q:
            return ans
    return "Sorry, I don't have an answer for that question."

# if __name__ == "__main__":
#     mcp.run()

# if __name__ == "__main__":
#     mcp.run(transport="http", host="127.0.0.1", port=8080)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8080)