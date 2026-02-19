from flask import Flask, render_template, request, redirect, session, url_for
import configparser
import subprocess
import os

# --- CONFIGURATION ---
CONFIG_FILE = "/home/tynatech/floor-wetness-detection/v1.2/config.ini"
DEVICE_SECTION = "CM5"

app = Flask(__name__)

# --- 1. SECURITY & SECRET KEY ---
def get_secret_key():
    if not os.path.exists(CONFIG_FILE):
        return "dev-fallback-secret-key"
    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    if DEVICE_SECTION in config and "secret" in config[DEVICE_SECTION]:
        return config[DEVICE_SECTION]["secret"]
    
    return config["DEFAULT"].get("secret", "dev-fallback-secret-key")

app.secret_key = get_secret_key()

# --- 2. USER CREDENTIALS ---
USERS = {
    "admin": "admin123",
    "user1": "password"
}

# --- 3. HELPER FUNCTIONS ---
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {
            "devEUI": "24E124136E172026 (Mock)",
            "appEUI": "A0B1C2D3E4F5 (Mock)",
            "interval": 20,
            "frequency": "IN865"
        }

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    section = config[DEVICE_SECTION] if DEVICE_SECTION in config else config["DEFAULT"]

    return {
        "devEUI": section.get("devEUI", "Unknown"),
        "appEUI": section.get("appEUI", "Not Set"),
        "interval": section.getint("interval", 5),
        "frequency": "IN865" 
    }

def save_interval(new_interval):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    if DEVICE_SECTION not in config:
        config.add_section(DEVICE_SECTION)
        
    config[DEVICE_SECTION]["interval"] = str(new_interval)
    
    with open(CONFIG_FILE, "w") as f:
        config.write(f)

def update_cronjob():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    if DEVICE_SECTION in config:
        interval = config[DEVICE_SECTION].get("interval", "5")
    else:
        interval = "5"

    cron_line = (
        f"*/{interval} * * * * "
        f"cd /home/tynatech/floor-wetness-detection/v1.2 && "
        f"/home/tynatech/venv/bin/python3 main.py >> "
        f"/home/tynatech/logs/floor-wetness-detection-cron.log 2>&1"
    )

    try:
        subprocess.run(["crontab", "-"], input=cron_line + "\n", text=True, check=True)
    except Exception as e:
        print(f"Failed to update cronjob: {e}")

# --- 4. ROUTES ---

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            session['user'] = username
            return redirect(url_for('index'))
        else:
            error = "Invalid Credentials"
            
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == "POST":
        try:
            val = request.form.get("interval")
            if val:
                new_interval = int(val)
                save_interval(new_interval)
                update_cronjob()
        except ValueError:
            pass 
            
        return redirect("/")

    cfg = load_config()
    return render_template("index.html", **cfg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

