import time, json, requests
import struct, serial
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

url = config['CM5']['UbidotsUrl']
token = config['CM5']['UbidotsToken']
devEUI = config['CM5']['devEUI']

def send_data_http(payload):

    url = f"{url}/{devEUI}/?token={token}"

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)

        if response.status_code in [200, 201]:
            print(f"Data successfully sent to {device_label}")
            print(response.text)
        else:
            print(f"Failed with status {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"HTTP Error: {e}")

def send_data_uart(payload):
    coverage_percent = payload["COVERAGE"]              # float
    num_detections = payload["DETECTIONS"]              # int
    wetness = payload["WETNESS"]                        # int


    try:
        # --- Setup UART ---
        ser = serial.Serial('/dev/serial0', 9600, timeout=1)

        # --- Prepare compact binary payload ---
        # Byte[0] = coverage % (0-100)
        # Byte[1] = number of detections (0-255)

        # Header Byte
        # payload = struct.pack("BBBB", 0xAA, int(coverage_percent), num_detections, wetness)

        payload = struct.pack("<BfBB", 0xAA, coverage_percent, num_detections, wetness)
        # --- Send data over UART ---
        ser.write(payload)

        print("Payload: ", payload)
        # payload = struct.pack("BBB", int(coverage_percent), num_detections, wetness)
        # payload = struct.pack("BB", int(coverage_percent), num_detections)



        print(f"Sent binary data -> Coverage: {float(coverage_percent)}%, Detections: {num_detections}, Wetness: {wetness}")

        ser.close()


    except Exception as SerialError:
        print("Failed to send data over Serial: \n", SerialError)
