import os, datetime, subprocess
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

base_dir = config['CM4']['BaseDir']

def capture_image():
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    os.makedirs(os.path.join(base_dir, "images"), exist_ok=True)
    filename = os.path.join(base_dir, "images", f"photo_{timestamp}.jpg")
    cmd = ["rpicam-still", "-t", "1000", "-o", filename]
    try:
        subprocess.run(cmd, check=True)
        print(f"Photo saved as {filename}")
        return filename
    except subprocess.CalledProcessError as e:
        return None

