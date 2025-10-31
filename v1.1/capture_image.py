import os, datetime, subprocess
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

base_dir = config['CM5']['BaseDir']

def capture_image():
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(base_dir, "images", f"photo_{timestamp}.jpg")
    cmd = ["rpicam-still", "-t", "1000", "-o", filename]
    try:
        subprocess.run(cmd, check=True)
        print(f"Photo saved as {filename}")
        return filename
    except subprocess.CalledProcessError as e:
        return None

