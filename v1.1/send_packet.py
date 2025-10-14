import time, json, requests
import struct, serial

def send_data_http(payload):
    device_label = "deviceLabel"
    ubidots_token = "BBUS-12bzjWk4"

    url = f"https://app.iotyn.in/api/v1.6/devices/{device_label}/?token={ubidots_token}"

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
    ser = serial.Serial('/dev/serial0', 9600, timeout=1)

    payload = struct.pack("BBB", int(coverage_percent*100), num_detections, wetness)
    # payload = struct.pack("BB", int(coverage_percent), num_detections)

    ser.write(payload)
    print(f"Sent binary data -> Coverage: {int(coverage_percent)}%, Detections: {num_detections}")

    ser.close()




