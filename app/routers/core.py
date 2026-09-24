import time
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.carparks import carparks, sample_and_rank, NUM_CARPARKS
from app.logs import log_request


router = APIRouter()
MAX_N = 100

@router.get("/api/find-carparks")
async def find_carparks(uuid: str = Query(...), n: int = Query(...)):
    if n <= 0:
        return JSONResponse(status_code=400, content={"uuid": uuid, "status": "error", "msg": "n must be positive"})
    if n > MAX_N or n > NUM_CARPARKS:
        return JSONResponse(status_code=400, content={"uuid": uuid, "status": "error", "msg": "n too large"})

    log_request(uuid)

    start = time.perf_counter()
    ranked = await sample_and_rank(2 * n)
    top_n = ranked[:n]
    elapsed_ms = (time.perf_counter() - start) * 1000

    return {
        "uuid": uuid,
        "status": "success",
        "msg": "success",
        "speed_inference": f"{elapsed_ms:.1f} ms",
        "requested_n": n,
        "results": [
            {
                "carpark_id": c["carpark_id"],
                "name": c["name"],
                "available_spaces": c["available_spaces"],
                "confidence_score": c["confidence_score"],
            }
            for c in top_n
        ],
    }

@router.get("/api/annotate-carpark")
def annotate_carpark(carpark_id: str = Query(...)):
    cp = carparks.get(carpark_id)
    if cp is None:
        return JSONResponse(status_code=404, content={"carpark_id": carpark_id, "status": "error", "msg": "unknown carpark_id"})
    if cp["last_annotated_image_b64"] is None:
        return JSONResponse(status_code=404, content={"carpark_id": carpark_id, "status": "error", "msg": "no image available yet, call find-carparks first"})

    return {
        "carpark_id": carpark_id,
        "status": "success",
        "msg": "success",
        "image_base64": cp["last_annotated_image_b64"],
    }