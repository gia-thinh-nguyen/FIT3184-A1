import asyncio
import random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from app.inference import run_inference

NUM_CARPARKS = 30
IMAGE_DIR = Path(__file__).parent.parent / "images"
IMAGE_PATHS = list(IMAGE_DIR.glob("*.jpg")) + list(IMAGE_DIR.glob("*.png"))

executor = ThreadPoolExecutor(max_workers=8)

carparks = {
    f"CBD_{i:03d}": {
        "carpark_id": f"CBD_{i:03d}",
        "name": f"Street {i}",
        "available_spaces": None,
        "total_spaces": None,
        "confidence_score": None,
        "last_annotated_image_b64": None,
    }
    for i in range(1, NUM_CARPARKS + 1)
}


def _query_one_carpark_sync(carpark_id: str):
    cp = carparks[carpark_id]
    image_path = random.choice(IMAGE_PATHS)

    available, total, confidence, annotated_b64 = run_inference(str(image_path))

    cp["available_spaces"] = available
    cp["total_spaces"] = total
    cp["confidence_score"] = confidence
    cp["last_annotated_image_b64"] = annotated_b64

    return cp


async def sample_and_rank(sample_size: int):
    ids = random.sample(list(carparks.keys()), min(sample_size, len(carparks)))

    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(executor, _query_one_carpark_sync, cid) for cid in ids]
    sampled = await asyncio.gather(*tasks)

    sampled = list(sampled)
    sampled.sort(key=lambda c: c["available_spaces"], reverse=True)
    return sampled