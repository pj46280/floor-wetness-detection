import os, datetime, subprocess

def capture_image():
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    base_dir = "/home/tynatech/WetFloorDetection/v1.1" 
    filename = os.path.join(base_dir, "images", f"photo_{timestamp}.jpg")
    cmd = ["rpicam-still", "-t", "1000", "-o", filename]
    try:
        subprocess.run(cmd, check=True)
        print(f"Photo saved as {filename}")
        return filename
    except subprocess.CalledProcessError as e:
        return None

