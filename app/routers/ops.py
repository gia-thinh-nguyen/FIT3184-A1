from fastapi import APIRouter
from app.carparks import carparks
from app.logs import count_requests_last_n_seconds

router = APIRouter()

@router.get("/api/ops/carparks")
def list_carparks():
    return {
        "status": "success",
        "carparks": [
            {
                "carpark_id": cp["carpark_id"],
                "name": cp["name"],
                "available_spaces": cp["available_spaces"],
            }
            for cp in carparks.values()
        ],
    }

@router.get("/api/ops/active-users")
def active_users():
    return {
        "status": "success",
        "window_seconds": 30,
        "user_count": count_requests_last_n_seconds(30),
    }