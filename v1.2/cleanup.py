import os
import shutil
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

base_dir = config['CM5']['BaseDir']

images_dir = os.path.join(base_dir, "images")
runs_dir = os.path.join(base_dir, "runs")   # YOLO output

def cleanup():
    print("\n--- Running Cleanup ---")

    # 1️⃣ Remove all images
    if os.path.exists(images_dir):
        try:
            for f in os.listdir(images_dir):
                file_path = os.path.join(images_dir, f)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print("✔ Cleared images/")
        except Exception as e:
            print("⚠ Error clearing images/:", e)

    # 2️⃣ Remove YOLO runs directory entirely
    if os.path.exists(runs_dir):
        try:
            shutil.rmtree(runs_dir)
            print("✔ Removed runs/ directory")
        except Exception as e:
            print("⚠ Error removing runs/:", e)

    print("✔ Cleanup complete.\n")

    # 3️⃣ Recreate runs/ cleanly
'''
    try:
        os.makedirs(runs_dir, exist_ok=True)
    except:
        pass
'''


