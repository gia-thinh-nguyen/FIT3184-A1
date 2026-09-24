from pathlib import Path
from ultralytics import YOLO
from PIL import Image
import io
import base64

MODEL_PATH = Path(__file__).parent.parent / "model" / "model.pt"
model = YOLO(str(MODEL_PATH))


def run_inference(image_path: str):
    """
    Returns (available_spaces, total_spaces, avg_confidence, annotated_image_b64)
    based on this model's own 'empty'/'occupied' classes.
    """
    results = model.predict(image_path, verbose=False)
    result = results[0]

    empty_confidences = []
    occupied_count = 0

    for box in result.boxes:
        label = result.names[int(box.cls[0].item())]
        conf = float(box.conf[0].item())
        if label == "empty":
            empty_confidences.append(conf)
        elif label == "occupied":
            occupied_count += 1

    available_spaces = len(empty_confidences)
    total_spaces = available_spaces + occupied_count
    avg_confidence = round(sum(empty_confidences) / len(empty_confidences), 4) if empty_confidences else 0.0

    annotated_img = Image.fromarray(result.plot()[:, :, ::-1])
    buf = io.BytesIO()
    annotated_img.save(buf, format="PNG")
    annotated_b64 = base64.b64encode(buf.getvalue()).decode("ascii")

    return available_spaces, total_spaces, avg_confidence, annotated_b64