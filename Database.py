import uuid
import math
from datetime import datetime, time
from decimal import Decimal
import re

class Database:
    def __init__(self) -> None:
        self.db = {}

    def validate_receipt(self, receipt):
        """
        Validate the provided receipt against the provided regular expressions

        Args: 
            receipt: Provided receipt
        Returns:
            boolean indicating if receipt is valid or not
        """
        validation_res = False
        if re.fullmatch("^[\\w\\s\\-&]+$", receipt.retailer) != None and re.fullmatch("^\\d+\\.\\d{2}$", receipt.total) != None:
            for item in receipt.items:
                if not re.fullmatch("^[\\w\\s\\-]+$", item.shortDescription) or not re.fullmatch("^\\d+\\.\\d{2}$", item.price):
                    validation_res = False
        validation_res = True
        return validation_res


    def ingest_data(self, receipt) -> str:
        """
        Ingests the provided receipt data into the in-memory database

        Args: 
            receipt: Provided receipt
        Returns:
            Generated UUID for the receipt
        """
        try:
            if not self.validate_receipt(receipt):
                raise ValueError("Invalid receipt submitted")
            
            receipt_id = uuid.uuid4()
            
            # Check for ID collision
            if receipt_id in self.db:
                receipt_id = uuid.uuid4()

            self.db[str(receipt_id)] = receipt
            return receipt_id
        except Exception as ex:
            raise ex
    
    def retrieve_receipt_points(self, receipt_id: str) -> dict:
        """
        Retrieves the points earned by the receipt corresponding to the provided receipt_id

        Args: 
            receipt_id: ID corresponding to receipt for which to retrieve points
        Returns:
            Points earned by thee receipt queried
        """
        if receipt_id not in self.db:
            raise ValueError("Receipt {} not found".format(receipt_id))
        
        receipt_points = self.calculate_receipt_points(self.db[receipt_id])
        return receipt_points
    
    def calculate_receipt_points(self, receipt) -> int:
        """
        Helper method to calculate the points earned by the provided receipt as specified in the provided criteria

        Args: 
            receipt: Receipt object for which to calculate points
        Returns:
            Calculated sum of points earned by the receipt
        """
        retailer = receipt.retailer
        total = Decimal(receipt.total)
        items = receipt.items
        purchase_date = datetime.strptime(receipt.purchaseDate, "%Y-%m-%d").date()
        purchase_time = datetime.strptime(receipt.purchaseTime, "%H:%M").time()

        receipt_points = 0

        alnum = 0
        for char in retailer:
            if char.isalnum():
                alnum += 1

        receipt_points += alnum

        if total == int(total):
            receipt_points += 50
        
        if total % Decimal(0.25) == 0:
            receipt_points += 25

        num_items = len(items)
        num_pair_items = num_items // 2
        receipt_points += (num_pair_items * 5)

        for item in items:
            if len(item.shortDescription.strip()) % 3 == 0:
                item_points = Decimal(item.price) * Decimal(0.2)
                receipt_points += math.ceil(item_points)

        day = purchase_date.strftime("%d")

        if int(day) % 2 == 1:
            receipt_points += 6

        start_time = time(14, 0, 0)
        end_time = time(16, 0, 0)

        if start_time < purchase_time < end_time:
            receipt_points += 10

        return receipt_points