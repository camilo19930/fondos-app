def fundEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name":  item["name"],
        "category":  item["category"],
        "minimum_amount":  item["minimum_amount"]        
    }
    
def fundsEntity(entity) -> list:
    return [fundEntity(item) for item in entity]