def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name":  item["name"],
        "email":  item["email"],
        "telefono":  item["telefono"],
        "fondo_actual": item["fondo_actual"], 
        "historico": item["historico"],   
        "password":  item["password"],
        "saldo":  item["saldo"]
    }
def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]