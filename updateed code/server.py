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



##jokhendra sir code for an updates tools in his mcp server

# import { Injectable, Logger } from '@nestjs/common';
# import { APIClientService } from '../services/api-client.service';
# import { MCPAuthService, MCPAuthGuard } from '../services/auth.service';
# import { MCPToolResult, SearchParams } from '../types/api-types';

# // MCP Tool interface definition
# export interface Tool {
#   name: string;
#   description: string;
#   inputSchema: {
#     type: 'object';
#     properties: Record<string, any>;
#     required?: string[];
#     anyOf?: Array<{ required: string[] }>;
#   };
# }

# @Injectable()
# export class ProductTools {
#   private readonly logger = new Logger(ProductTools.name);
#   private readonly authGuard: MCPAuthGuard;

#   constructor(
#     private readonly apiClient: APIClientService,
#     private readonly authService: MCPAuthService,
#   ) {
#     this.authGuard = new MCPAuthGuard(this.authService);
#   }

#   // Tool definitions
#   static getToolDefinitions(): Tool[] {
#     return [
#       {
#         name: 'search_products',
#         description:
#           'Search for products with advanced filtering options including category, brand, price range, and more',
#         inputSchema: {
#           type: 'object',
#           properties: {
#             query: {
#               type: 'string',
#               description:
#                 'Search query string to find products by name, description, or keywords',
#             },
#             category: {
#               type: 'string',
#               description: 'Category slug to filter products by category',
#             },
#             brand: {
#               type: 'string',
#               description: 'Brand ID or slug to filter products by brand',
#             },
#             minPrice: {
#               type: 'number',
#               description: 'Minimum price filter (inclusive)',
#             },
#             maxPrice: {
#               type: 'number',
#               description: 'Maximum price filter (inclusive)',
#             },
#             inStock: {
#               type: 'boolean',
#               description: 'Filter to show only products that are in stock',
#             },
#             featured: {
#               type: 'boolean',
#               description: 'Filter to show only featured products',
#             },
#             tags: {
#               type: 'array',
#               items: { type: 'string' },
#               description: 'Array of tags to filter products',
#             },
#             sortBy: {
#               type: 'string',
#               enum: [
#                 'relevance',
#                 'price',
#                 'name',
#                 'rating',
#                 'popularity',
#                 'newest',
#                 'discount',
#               ],
#               description: 'Sort products by specified criteria',
#             },
#             sortOrder: {
#               type: 'string',
#               enum: ['asc', 'desc'],
#               description: 'Sort order (ascending or descending)',
#             },
#             page: {
#               type: 'number',
#               default: 1,
#               minimum: 1,
#               description: 'Page number for pagination',
#             },
#             limit: {
#               type: 'number',
#               default: 10,
#               minimum: 1,
#               maximum: 100,
#               description: 'Number of products per page (max 100)',
#             },
#           },
#           required: [],
#         },
#       },
#       {
#         name: 'get_product_details',
#         description:
#           'Get detailed information about a specific product by ID or slug',
#         inputSchema: {
#           type: 'object',
#           properties: {
#             productId: {
#               type: 'string',
#               description: 'Product ID to fetch details for',
#             },
#             slug: {
#               type: 'string',
#               description: 'Product slug to fetch details for',
#             },
#           },
#           anyOf: [{ required: ['productId'] }, { required: ['slug'] }],
#         },
#       },
#       {
#         name: 'get_featured_products',
#         description: 'Get a list of featured products',
#         inputSchema: {
#           type: 'object',
#           properties: {
#             limit: {
#               type: 'number',
#               default: 10,
#               minimum: 1,
#               maximum: 50,
#               description: 'Number of featured products to return (max 50)',
#             },
#           },
#         },
#       },
#       {
#         name: 'get_products_by_category',
#         description: 'Get products within a specific category',
#         inputSchema: {
#           type: 'object',
#           properties: {
#             categorySlug: {
#               type: 'string',
#               description: 'Category slug to fetch products from',
#             },
#             page: {
#               type: 'number',
#               default: 1,
#               minimum: 1,
#               description: 'Page number for pagination',
#             },
#             limit: {
#               type: 'number',
#               default: 20,
#               minimum: 1,
#               maximum: 100,
#               description: 'Number of products per page',
#             },
#             sortBy: {
#               type: 'string',
#               enum: ['price', 'name', 'rating', 'popularity', 'newest'],
#               description: 'Sort products by specified criteria',
#             },
#           },
#           required: ['categorySlug'],
#         },
#       },
#       {
#         name: 'get_products_by_brand',
#         description: 'Get products from a specific brand',
#         inputSchema: {
#           type: 'object',
#           properties: {
#             brandSlug: {
#               type: 'string',
#               description: 'Brand slug to fetch products from',
#             },
#             page: {
#               type: 'number',
#               default: 1,
#               minimum: 1,
#               description: 'Page number for pagination',
#             },
#             limit: {
#               type: 'number',
#               default: 20,
#               minimum: 1,
#               maximum: 100,
#               description: 'Number of products per page',
#             },
#             sortBy: {
#               type: 'string',
#               enum: ['price', 'name', 'rating', 'popularity', 'newest'],
#               description: 'Sort products by specified criteria',
#             },
#           },
#           required: ['brandSlug'],
#         },
#       },
#     ];
#   }

#   // Tool handlers
#   async handleSearchProducts(
#     args: any,
#     apiKey: string,
#     userToken?: string,
#   ): Promise<MCPToolResult> {
#     try {
#       // Validate authentication
#       const userContext = await this.authGuard.validateRequest(
#         apiKey,
#         userToken,
#       );

#       // Build search parameters
#       const searchParams: SearchParams = {
#         query: args.query,
#         categorySlug: args.category,
#         brandId: args.brand,
#         minPrice: args.minPrice,
#         maxPrice: args.maxPrice,
#         inStock: args.inStock,
#         featured: args.featured,
#         tags: args.tags,
#         sortBy: args.sortBy,
#         sortOrder: args.sortOrder,
#         page: args.page || 1,
#         limit: args.limit || 10,
#       };

#       // Execute search
#       const response = await this.apiClient.searchProducts(searchParams);

#       if (!response.success) {
#         return this.createErrorResult(
#           'SEARCH_FAILED',
#           response.error || 'Failed to search products',
#         );
#       }

#       // Format response
#       const products = response.data;
#       const pagination = response.pagination;

#       let resultText = '';

#       if (args.query) {
#         resultText += Search results for "${args.query}"\n;
#       } else {
#         resultText += 'Product search results\n';
#       }

#       if (pagination) {
#         resultText += Found ${pagination.total} products (Page ${pagination.page}/${pagination.totalPages})\n\n;
#       }

#       if (products.length === 0) {
#         resultText += 'No products found matching your criteria.';
#       } else {
#         products.forEach((product, index) => {
#           resultText += ${index + 1}. ${product.title}\n;
#           resultText += `   ID: ${product.id}\n`;
#           resultText += `   Price: $${product.price}`;
#           if (product.comparePrice && product.comparePrice > product.price) {
#             resultText += ` (was $${product.comparePrice})`;
#           }
#           resultText += \n;
#           resultText += `   Stock: ${product.stock} available\n`;
#           if (product.brand) {
#             resultText += `   Brand: ${product.brand.name}\n`;
#           }
#           if (product.category) {
#             resultText += `   Category: ${product.category.name}\n`;
#           }
#           if (product.ratings > 0) {
#             resultText += `   Rating: ${product.ratings}/5 (${product.reviewCount} reviews)\n`;
#           }
#           if (product.description) {
#             const shortDesc =
#               product.description.length > 100
#                 ? product.description.substring(0, 100) + '...'
#                 : product.description;
#             resultText += `   Description: ${shortDesc}\n`;
#           }
#           resultText += '\n';
#         });
#       }

#       this.logger.log(
#         Product search completed: ${products.length} results for user ${userContext?.userId || 'system'},
#       );

#       return {
#         content: [
#           {
#             type: 'text',
#             text: resultText,
#           },
#           {
#             type: 'text',
#             text: \nDetailed JSON data:\n${JSON.stringify(response, null, 2)},
#           },
#         ],
#       };
#     } catch (error) {
#       this.logger.error('Product search failed', error);
#       return this.createErrorResult('SEARCH_ERROR', error.message);
#     }
#   }

#   async handleGetProductDetails(
#     args: any,
#     apiKey: string,
#     userToken?: string,
#   ): Promise<MCPToolResult> {
#     try {
#       // Validate authentication
#       const userContext = await this.authGuard.validateRequest(
#         apiKey,
#         userToken,
#       );

#       let response;

#       if (args.productId) {
#         response = await this.apiClient.getProductById(args.productId);
#       } else if (args.slug) {
#         response = await this.apiClient.getProductBySlug(args.slug);
#       } else {
#         return this.createErrorResult(
#           'INVALID_INPUT',
#           'Either productId or slug must be provided',
#         );
#       }

#       if (!response.success) {
#         return this.createErrorResult(
#           'PRODUCT_NOT_FOUND',
#           response.error || 'Product not found',
#         );
#       }

#       const product = response.data;

#       let resultText = Product Details: ${product.title}\n;
#       resultText += =====================================\n\n;
#       resultText += ID: ${product.id}\n;
#       resultText += SKU: ${product.sku}\n;
#       resultText += Price: $${product.price};
#       if (product.comparePrice && product.comparePrice > product.price) {
#         const discount = Math.round(
#           ((product.comparePrice - product.price) / product.comparePrice) * 100,
#         );
#         resultText += ` (${discount}% off from $${product.comparePrice})`;
#       }
#       resultText += \n;
#       resultText += Stock: ${product.stock} available\n;

#       if (product.brand) {
#         resultText += Brand: ${product.brand.name}\n;
#       }

#       if (product.category) {
#         resultText += Category: ${product.category.name}\n;
#       }

#       if (product.ratings > 0) {
#         resultText += Rating: ${product.ratings}/5 stars (${product.reviewCount} reviews)\n;
#       }

#       resultText += Status: ${product.status}\n;
#       resultText += Featured: ${product.featured ? 'Yes' : 'No'}\n;

#       if (product.tags && product.tags.length > 0) {
#         resultText += Tags: ${product.tags.join(', ')}\n;
#       }

#       if (product.description) {
#         resultText += \nDescription:\n${product.description}\n;
#       }

#       if (product.variants && product.variants.length > 0) {
#         resultText += \nVariants (${product.variants.length}):\n;
#         product.variants.forEach((variant, index) => {
#           resultText += `  ${index + 1}. ${variant.title} - $${variant.price} (Stock: ${variant.stock})\n`;
#         });
#       }

#       if (product.specifications && product.specifications.length > 0) {
#         resultText += \nSpecifications:\n;
#         product.specifications.forEach((spec) => {
#           resultText += `  ${spec.name}: ${spec.value}\n`;
#         });
#       }

#       this.logger.log(
#         Product details retrieved for ${args.productId || args.slug} by user ${userContext?.userId || 'system'},
#       );

#       return {
#         content: [
#           {
#             type: 'text',
#             text: resultText,
#           },
#           {
#             type: 'text',
#             text: \nComplete product data:\n${JSON.stringify(product, null, 2)},
#           },
#         ],
#       };
#     } catch (error) {
#       this.logger.error('Get product details failed', error);
#       return this.createErrorResult('PRODUCT_ERROR', error.message);
#     }
#   }

#   async handleGetFeaturedProducts(
#     args: any,
#     apiKey: string,
#     userToken?: string,
#   ): Promise<MCPToolResult> {
#     try {
#       // Validate authentication
#       const userContext = await this.authGuard.validateRequest(
#         apiKey,
#         userToken,
#       );

#       const response = await this.apiClient.getFeaturedProducts(
#         args.limit || 10,
#       );

#       if (!response.success) {
#         return this.createErrorResult(
#           'FEATURED_PRODUCTS_FAILED',
#           response.error || 'Failed to get featured products',
#         );
#       }

#       const products = response.data;

#       let resultText = Featured Products (${products.length} items)\n;
#       resultText += =======================================\n\n;

#       products.forEach((product, index) => {
#         resultText += ${index + 1}. ${product.title}\n;
#         resultText += `   Price: $${product.price}\n`;
#         resultText += `   Stock: ${product.stock}\n`;
#         if (product.ratings > 0) {
#           resultText += `   Rating: ${product.ratings}/5\n`;
#         }
#         resultText += '\n';
#       });

#       this.logger.log(
#         Featured products retrieved (${products.length} items) for user ${userContext?.userId || 'system'},
#       );

#       return {
#         content: [
#           {
#             type: 'text',
#             text: resultText,
#           },
#         ],
#       };
#     } catch (error) {
#       this.logger.error('Get featured products failed', error);
#       return this.createErrorResult('FEATURED_ERROR', error.message);
#     }
#   }

#   async handleGetProductsByCategory(
#     args: any,
#     apiKey: string,
#     userToken?: string,
#   ): Promise<MCPToolResult> {
#     try {
#       // Validate authentication
#       const userContext = await this.authGuard.validateRequest(
#         apiKey,
#         userToken,
#       );

#       const params = {
#         page: args.page,
#         limit: args.limit,
#         sortBy: args.sortBy,
#       };

#       const response = await this.apiClient.getProductsByCategory(
#         args.categorySlug,
#         params,
#       );

#       if (!response.success) {
#         return this.createErrorResult(
#           'CATEGORY_PRODUCTS_FAILED',
#           response.error || 'Failed to get products by category',
#         );
#       }

#       const products = response.data;
#       const pagination = response.pagination;

#       let resultText = Products in Category: ${args.categorySlug}\n;
#       resultText += =====================================\n;

#       if (pagination) {
#         resultText += Found ${pagination.total} products (Page ${pagination.page}/${pagination.totalPages})\n\n;
#       }

#       products.forEach((product, index) => {
#         resultText += ${index + 1}. ${product.title} - $${product.price}\n;
#       });

#       this.logger.log(
#         Category products retrieved for ${args.categorySlug} by user ${userContext?.userId || 'system'},
#       );

#       return {
#         content: [
#           {
#             type: 'text',
#             text: resultText,
#           },
#         ],
#       };
#     } catch (error) {
#       this.logger.error('Get products by category failed', error);
#       return this.createErrorResult('CATEGORY_ERROR', error.message);
#     }
#   }

#   async handleGetProductsByBrand(
#     args: any,
#     apiKey: string,
#     userToken?: string,
#   ): Promise<MCPToolResult> {
#     try {
#       // Validate authentication
#       const userContext = await this.authGuard.validateRequest(
#         apiKey,
#         userToken,
#       );

#       const params = {
#         page: args.page,
#         limit: args.limit,
#         sortBy: args.sortBy,
#       };

#       const response = await this.apiClient.getProductsByBrand(
#         args.brandSlug,
#         params,
#       );

#       if (!response.success) {
#         return this.createErrorResult(
#           'BRAND_PRODUCTS_FAILED',
#           response.error || 'Failed to get products by brand',
#         );
#       }

#       const products = response.data;
#       const pagination = response.pagination;

#       let resultText = Products by Brand: ${args.brandSlug}\n;
#       resultText += ==================================\n;

#       if (pagination) {
#         resultText += Found ${pagination.total} products (Page ${pagination.page}/${pagination.totalPages})\n\n;
#       }

#       products.forEach((product, index) => {
#         resultText += ${index + 1}. ${product.title} - $${product.price}\n;
#       });

#       this.logger.log(
#         Brand products retrieved for ${args.brandSlug} by user ${userContext?.userId || 'system'},
#       );

#       return {
#         content: [
#           {
#             type: 'text',
#             text: resultText,
#           },
#         ],
#       };
#     } catch (error) {
#       this.logger.error('Get products by brand failed', error);
#       return this.createErrorResult('BRAND_ERROR', error.message);
#     }
#   }

#   private createErrorResult(code: string, message: string): MCPToolResult {
#     return {
#       content: [
#         {
#           type: 'text',
#           text: Error: ${message},
#         },
#       ],
#       isError: true,
#     };
#   }
# }