def transactionEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name":  item["name"],
        "category":  item["category"],
        "minimum_amount":  item["minimum_amount"]        
    }
def transactionsEntity(entity) -> list:
    return [transactionEntity(item) for item in entity]