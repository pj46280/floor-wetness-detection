# -*- coding: utf-8 -*-
import time
import serial
from ultralytics import YOLO
from capture_image import capture_image
from PIL import Image
import struct

# --- Setup UART ---
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

# --- Load YOLO model ---
model = YOLO("WetFloorDetection-v1.1.onnx")

# --- Capture image ---
filename = capture_image()
# filename = "/home/tynatech/WetFloorDetection/v1.1/images/photo_20250930-140213.jpg"

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
        continue

    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        box_area = (x2 - x1) * (y2 - y1)
        total_box_area += box_area
        num_detections += 1

# --- Calculate total coverage ---
coverage_percent = (total_box_area / img_area) * 100
coverage_percent = min(max(coverage_percent, 0), 100)

print(f"Detections: {num_detections}, Coverage: {coverage_percent:.2f}%")

# --- Prepare compact binary payload ---
# Byte[0] = coverage % (0-100)
# Byte[1] = number of detections (0-255)
payload = struct.pack("BB", int(coverage_percent), num_detections)

# --- Send data over UART ---
ser.write(payload)
print(f"Sent binary data -> Coverage: {int(coverage_percent)}%, Detections: {num_detections}")

ser.close()
