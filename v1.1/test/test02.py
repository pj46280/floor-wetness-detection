import serial
import time
import random

# Setup UART
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

while True:
    temperature = round(25 + random.uniform(-2, 2), 2)  # dummy data
    data = f"TEMP:{temperature}\n"
    ser.write(data.encode())
    print(f"Sent: {data.strip()}")
    time.sleep(5)
