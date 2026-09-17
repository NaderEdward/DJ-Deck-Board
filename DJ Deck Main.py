import os, sys, time
import serial
from pyo import Server, SPlayer, Biquadx, Sig

# ---------- Configurable Presets & Conditions ----------
PRESET_TRIGGER_DIST_A = 20  # Max distance (cm) to trigger Deck A
PRESET_TRIGGER_DIST_B = 20  # Max distance (cm) to trigger Deck B
PRESET_PITCH_TOUCH = 1.5    # Pitch setting when touchpad is pressed
PRESET_PITCH_NORMAL = 1.0   # Default pitch setting

SERIAL_PORT = 'COM3'        # Update to match your Arduino port
BAUD_RATE = 9600

# ---------- Default Audio Configuration ----------
INITIAL_TEXT = """PATH_A = C:\\Users\\nader\\Desktop\\DJ Deck Python\\f.mp3
VOL_A = 0.0
PITCH_A = 1.0
FILT_A = 12000

PATH_B = C:\\Users\\nader\\Desktop\\DJ Deck Python\\f.mp3
VOL_B = 0.0
PITCH_B = 1.0
FILT_B = 12000
"""

# ---------- Serial Initialization ----------
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.01)
    print(f"[*] Connected to Arduino on {SERIAL_PORT}")
except Exception as e:
    ser = None
    print(f"[!] Serial warning: {e}")

# ---------- Audio Engine Setup ----------
s = Server().boot()
s.start()

def exists_path(p): 
    return bool(p) and os.path.exists(p)

def make_player(path, speed, mul):
    try: 
        return SPlayer(path, speed=float(speed), loop=True, mul=float(mul))
    except Exception: 
        return None

# State Variables
playerA = None; pathA = ""; volA = 0.0; pitchA = 1.0; filtA_freq = 12000.0
playerB = None; pathB = ""; volB = 0.0; pitchB = 1.0; filtB_freq = 12000.0
filtA = None; filtB = None
masterA = Sig(0.0); masterB = Sig(0.0)
current_path_A = ""; current_path_B = None
vars_dict = {}

def parse_vars_from_text(text):
    for line in text.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            vars_dict[k.strip()] = v.strip().strip('"').strip("'")

def apply_vars_from_text(text=""):
    global playerA, pathA, volA, pitchA, filtA_freq, filtA, current_path_A
    global playerB, pathB, volB, pitchB, filtB_freq, filtB, current_path_B
    
    if text:
        parse_vars_from_text(text)
    
    # --- Deck A ---
    pathA = vars_dict.get("PATH_A", "")
    volA = float(vars_dict.get("VOL_A", "0.0"))
    pitchA = float(vars_dict.get("PITCH_A", "1.0"))
    filtA_freq = float(vars_dict.get("FILT_A", "12000"))

    if pathA != current_path_A:
        if playerA: playerA.stop()
        if exists_path(pathA):
            playerA = make_player(pathA, pitchA, volA)
            if playerA:
                filtA = Biquadx(playerA, freq=filtA_freq, q=0.7, type=0).out()
                filtA.mul = masterA
                current_path_A = pathA

    if playerA:
        try: playerA.setSpeed(pitchA)
        except: pass
        masterA.value = volA
        if filtA: filtA.freq = filtA_freq

    # --- Deck B ---
    pathB = vars_dict.get("PATH_B", "")
    volB = float(vars_dict.get("VOL_B", "0.0"))
    pitchB = float(vars_dict.get("PITCH_B", "1.0"))
    filtB_freq = float(vars_dict.get("FILT_B", "12000"))

    if pathB != current_path_B:
        if playerB: playerB.stop()
        if exists_path(pathB):
            playerB = make_player(pathB, pitchB, volB)
            if playerB:
                filtB = Biquadx(playerB, freq=filtB_freq, q=0.7, type=0).out()
                filtB.mul = masterB
                current_path_B = pathB

    if playerB:
        try: playerB.setSpeed(pitchB)
        except: pass
        masterB.value = volB
        if filtB: filtB.freq = filtB_freq

# Initialize Audio System
apply_vars_from_text(INITIAL_TEXT)

# ---------- Raw Telemetry Processor ----------
def process_raw_telemetry(line):
    if "=" not in line:
        return
    
    sensor_id, raw_val = line.split("=", 1)
    sensor_id = sensor_id.strip()
    val = float(raw_val.strip())

    # Condition Logic: Check Ultrasonic Sensor 1 (Deck A trigger)
    if sensor_id == "US1":
        if val <= PRESET_TRIGGER_DIST_A:
            vars_dict["VOL_A"] = "0.9"
        else:
            vars_dict["VOL_A"] = "0.0"

    # Condition Logic: Check Ultrasonic Sensor 2 (Deck B trigger)
    elif sensor_id == "US2":
        if val <= PRESET_TRIGGER_DIST_B:
            vars_dict["VOL_B"] = "0.9"
        else:
            vars_dict["VOL_B"] = "0.0"

    # Condition Logic: Check Touchpad State
    elif sensor_id == "TOUCH":
        if val == 1.0:
            vars_dict["PITCH_A"] = str(PRESET_PITCH_TOUCH)
            vars_dict["PITCH_B"] = str(PRESET_PITCH_TOUCH)
        else:
            vars_dict["PITCH_A"] = str(PRESET_PITCH_NORMAL)
            vars_dict["PITCH_B"] = str(PRESET_PITCH_NORMAL)

    apply_vars_from_text()

# ---------- Main Loop ----------
print("[*] CLI Audio Decision Engine Active. Waiting for raw telemetry...")

try:
    while True:
        if ser and ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    process_raw_telemetry(line)
                    sys.stdout.write(f"\r[STATUS] VolA: {volA} | VolB: {volB} | Pitch: {pitchA}  ")
                    sys.stdout.flush()
            except Exception:
                pass
        time.sleep(0.005)
except KeyboardInterrupt:
    print("\n[-] Shutting down audio engine...")
    s.stop()
    if ser:
        ser.close()