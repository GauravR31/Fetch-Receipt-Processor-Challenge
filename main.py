from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date, time
from decimal import Decimal

class Item(BaseModel):
    shortDescription: str
    price: Decimal

class Receipt(BaseModel):
    retailer: str
    purchaseDate: date
    purchaseTime: time
    total: Decimal
    items: Item

app = FastAPI()

@app.get("/")
def hello_world():
    return {"msg": "Hello"}

@app.post("/receipts/process")
def process_receipt(receipt: Receipt):
    # TODO: Ingest receipt
    return receipt

@app.get("/receipts/{receipt_id}/points")
def get_receipt_points(receipt_id: str):
    # TODO: Calculate points and return
    return 0