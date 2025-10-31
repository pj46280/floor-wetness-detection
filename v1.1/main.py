import time, os
from ultralytics import YOLO
from capture_image import capture_image
from send_packet import send_data_http, send_data_uart
from PIL import Image
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

base_dir = config['CM5']['BaseDir']
path = os.path.join(base_dir, config['CM5']['Model'])

# --- Load YOLO model ---
model = YOLO(f"{path}")

# --- Capture or use existing image ---
filename = capture_image()

# --- Run inference ---
results = model(filename, save=True, imgsz=640, conf=0.25)

# --- Get image dimensions ---
image = Image.open(filename)
img_width, img_height = image.size
img_area = img_width * img_height

total_box_area = 0
num_detections = 0

for result in results:
    boxes = result.boxes
    if boxes is None or len(boxes) == 0:
        print("No detections found.")
        continue

    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        box_area = (x2 - x1) * (y2 - y1)
        total_box_area += box_area
        num_detections += 1

        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        label = result.names[cls_id]

        print(f"Detected {label} ({conf:.2f}) at [{x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f}] - Area: {box_area:.0f}px²")

# --- Calculate total coverage ---
coverage_percent = (total_box_area / img_area) * 100
print(f"\nTotal detection area covers: {coverage_percent:.2f}% of the image")

# Example format: COVERAGE:12.34, DETECTIONS:3
message = f"COVERAGE:{coverage_percent:.2f}, WETNESS:{1 if num_detections > 0 else 0}\n"
payload = {
    "WETNESS": 1 if num_detections > 0 else 0,  # int
    "COVERAGE": coverage_percent,               # float
    "DETECTIONS": num_detections                # int
}

send_data_http(payload)
send_data_uart(payload)


