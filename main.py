from fastapi import FastAPI, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from Database import Database
from typing import List

class Item(BaseModel):
    shortDescription: str
    price: str

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    total: str
    items: List[Item]

database = Database()

app = FastAPI()

# Custom exception handler to return 400 instead of 422 (FastAPI default for invalid parmeters)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(str(exc), status_code=400)

@app.get("/")
def hello_world():
    return {"msg": "Hello"}

@app.post("/receipts/process")
def process_receipt(receipt: Receipt, response: Response):
    """
    Submits a receipt for processing
    """
    try:
        receipt_id = database.ingest_data(receipt)
        return {"id": receipt_id}
    except ValueError as val_ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error:": str(val_ex)}
    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error:": ex.message}

@app.get("/receipts/{receipt_id}/points")
def get_receipt_points(receipt_id: str, response: Response):
    """
    Returns the points awarded for the receipt
    """
    try:
        receipt_points = database.retrieve_receipt_points(receipt_id)
        return {"points": receipt_points}
    except ValueError as val_ex:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error:": str(val_ex)}
    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error:": str(ex)}