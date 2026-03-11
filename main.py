from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()
products = [
    {"id":1,"name":"Wireless Mouse","price":499,"category":"electronics","in_stock":True},
    {"id":2,"name":"Keyboard","price":799,"category":"electronics","in_stock":True},
    {"id":3,"name":"Notebook","price":99,"category":"stationery","in_stock":True},
    {"id":4,"name":"Pen","price":20,"category":"stationery","in_stock":False},
]
@app.get("/products/filter")
def filter_products(min_price:int=None):

    result = []

    for p in products:
        if min_price is None or p["price"] >= min_price:
            result.append(p)

    return result
@app.get("/products/{product_id}/price")
def get_product_price(product_id:int):

    for product in products:
        if product["id"] == product_id:
            return {
                "name": product["name"],
                "price": product["price"]
            }

    return {"error":"Product not found"}
class CustomerFeedback(BaseModel):
    customer_name: str
    product_id: int
    rating: int
    comment: Optional[str] = None
feedback = []

@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):

    feedback.append(data)

    return {
        "message":"Feedback submitted",
        "total_feedback":len(feedback)
    }
@app.get("/products/summary")
def product_summary():

    total = len(products)

    in_stock = [p for p in products if p["in_stock"]]
    out_stock = [p for p in products if not p["in_stock"]]

    expensive = max(products, key=lambda x:x["price"])
    cheap = min(products, key=lambda x:x["price"])

    return {
        "total_products": total,
        "in_stock": len(in_stock),
        "out_of_stock": len(out_stock),
        "most_expensive": expensive["name"],
        "cheapest": cheap["name"]
    }
class OrderItem(BaseModel):
    product_id:int
    quantity:int

class BulkOrder(BaseModel):
    company_name:str
    items:List[OrderItem]
@app.post("/orders/bulk")
def bulk_order(order: BulkOrder):

    total = 0

    for item in order.items:

        for p in products:
            if p["id"] == item.product_id:
                total += p["price"] * item.quantity

    return {
        "company": order.company_name,
        "grand_total": total
    }
@app.get("/products")
def get_products():
    return products
@app.post("/products")
def add_product(product: dict):
    products.append(product)
    return {"message": "Product added", "product": product}
@app.put("/products/{product_id}")
def update_product(product_id: int, price: int = None, in_stock: bool = None):
    for p in products:
        if p["id"] == product_id:
            if price is not None:
                p["price"] = price
            if in_stock is not None:
                p["in_stock"] = in_stock
            return p
    return {"error": "Product not found"}
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            products.remove(p)
            return {"message": "Product deleted"}
    return {"error": "Product not found"}