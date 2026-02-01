import os
import webbrowser
import pyautogui
import cv2
import screen_brightness_control as sbc
import psutil
import shutil
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

PROCESS_NAMES = {
    # Browsers
    "chrome": "chrome.exe", "googlechrome": "chrome.exe", "google": "chrome.exe",
    "brave": "brave.exe", "bravebrowser": "brave.exe", 
    "edge": "msedge.exe", "msedge": "msedge.exe", "microsoftedge": "msedge.exe",
    "firefox": "firefox.exe", "mozilla": "firefox.exe",
    "opera": "opera.exe",

    # System & Tools
    "notepad": "notepad.exe",
    "calculator": "calc.exe", "calc": "calc.exe",
    "cmd": "cmd.exe", "terminal": "WindowsTerminal.exe",
    "explorer": "explorer.exe", "fileexplorer": "explorer.exe",
    "taskmanager": "Taskmgr.exe",

    # Media
    "spotify": "spotify.exe",
    "vlc": "vlc.exe", 

    # Coding
    "vscode": "Code.exe", "code": "Code.exe", "visualstudiocode": "Code.exe",
    "pycharm": "pycharm64.exe",
    "androidstudio": "studio64.exe",
    "intellij": "idea64.exe",
    "python": "python.exe",

    # Social
    "telegram": "Telegram.exe",
    "discord": "Discord.exe",
    "whatsapp": "WhatsApp.exe",
    "zoom": "Zoom.exe"
}

def get_browser_path(browser_name):
    """Finds browser executable dynamically without hardcoded paths."""
    browser_name = browser_name.lower().strip()
    
    exes = {
        "chrome": "chrome.exe",
        "google": "chrome.exe",
        "brave": "brave.exe", 
        "firefox": "firefox.exe",
        "mozilla": "firefox.exe",
        "edge": "msedge.exe",
        "msedge": "msedge.exe",
        "opera": "launcher.exe" 
    }
    
    executable = exes.get(browser_name, f"{browser_name}.exe")
    if not executable.endswith(".exe"): executable += ".exe"
    
  
    path = shutil.which(executable)
    if path: return path
    
   
    possible_roots = [
        os.environ.get("PROGRAMFILES"), 
        os.environ.get("PROGRAMFILES(X86)"),
        os.environ.get("LOCALAPPDATA") 
    ]
    
    common_subdirs = [
        "Google\\Chrome\\Application",
        "BraveSoftware\\Brave-Browser\\Application",
        "Microsoft\\Edge\\Application",
        "Mozilla Firefox",
        "Opera"
    ]
    
    for root in possible_roots:
        if not root: continue
        for subdir in common_subdirs:
            full_path = os.path.join(root, subdir, executable)
            if os.path.exists(full_path):
                return full_path
                
    return None


def capture_webcam():
    print("📸 Accessing Webcam...")
    try:
      
        for i in range(2):
            cam = cv2.VideoCapture(i)
            if cam.isOpened():
                ret, frame = cam.read()
                if ret:
                    file_path = os.path.join(os.getcwd(), "webcam_snap.jpg")
                    cv2.imwrite(file_path, frame)
                    cam.release()
                    return file_path
                cam.release()
        print("❌ No active camera found.")
        return None
    except Exception as e:
        print(f"Error accessing webcam: {e}")
        return None


def capture_screen():
    file_path = os.path.join(os.getcwd(), "screenshot.png")
    try:
        print("📸 Taking screenshot...")
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        return file_path
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return None


def record_audio(duration=10):
    """Records audio from the default microphone for specified duration (in seconds).
    Uses sounddevice library - Works on Windows Python 3.10 without C++ compiler!"""
    file_path = os.path.join(os.getcwd(), "audio_recording.wav")
    
    # Audio recording parameters
    SAMPLE_RATE = 44100  # CD quality (44.1kHz)
    CHANNELS = 1  # Mono recording
    
    print(f"🎤 Recording audio for {duration} seconds...")
    
    try:
        # Record audio using sounddevice (no compilation needed!)
        recording = sd.rec(
            int(duration * SAMPLE_RATE), 
            samplerate=SAMPLE_RATE, 
            channels=CHANNELS, 
            dtype='int16'
        )
        
        # Wait until recording is finished
        sd.wait()
        
        print("✅ Recording complete.")
        
        # Save the recorded audio as WAV file
        write(file_path, SAMPLE_RATE, recording)
        
        return file_path
        
    except Exception as e:
        print(f"❌ Error recording audio: {e}")
        return None


def system_sleep():
    print("💤 Going to sleep...")
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


def get_battery_status():
    try:
        battery = psutil.sensors_battery()
        if not battery:
            return "Cannot determine battery status (Device might be a Desktop)."
        
        percent = battery.percent
        charging = battery.power_plugged
        status = "Charging ⚡" if charging else "Discharging 🔋"
        
        return f"Battery is at {percent}% and is currently {status}."
    except Exception as e:
        return f"Error reading battery: {e}"


def get_system_health():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        ram_available = round(ram.available / (1024 * 1024 * 1024), 2)
        return f"🖥️ **System Health:**\nCPU Usage: {cpu_usage}%\nRAM Usage: {ram_usage}% ({ram_available} GB free)"
    except Exception as e:
        return f"Error reading system health: {e}"


def open_browser(url, browser_name="default"):
    print(f"🌐 Request to open '{url}' in '{browser_name}'")
    
    try:
      
        if not browser_name or browser_name.lower() == "default":
            webbrowser.open(url)
            return

       
        path = get_browser_path(browser_name)
        
        if path:
            print(f"   -> Found browser at: {path}")
            
            webbrowser.register(browser_name, None, webbrowser.BackgroundBrowser(path))
            webbrowser.get(browser_name).open(url)
        else:
            print(f"⚠️ Could not find '{browser_name}'. Falling back to default.")
            webbrowser.open(url)
            
    except Exception as e:
        print(f"Error opening browser: {e}")
        webbrowser.open(url)

def close_application(app_name):
    
    clean_name = app_name.lower()
    for word in ["the ", "app ", "application ", "close ", "open "]:
        clean_name = clean_name.replace(word, "")
    
    
    app_key = clean_name.strip().replace(" ", "")
    
  
    if app_key in PROCESS_NAMES:
        exe_name = PROCESS_NAMES[app_key]
    else:
        exe_name = f"{app_key}.exe"
        
    print(f"💀 Killing process target: {exe_name}")
    

    try:
        os.system(f"taskkill /f /im {exe_name} /t")
    except Exception as e:
        print(f"Error closing app: {e}")

def open_file_path(path):
    try:
        if "download" in path.lower():
            path = os.path.join(os.path.expanduser("~"), "Downloads")
        elif "desktop" in path.lower():
            path = os.path.join(os.path.expanduser("~"), "Desktop")
        elif "c drive" in path.lower() or "c:" in path.lower():
            path = "C:/"
            
        if os.path.exists(path):
            os.startfile(path)
        else:
            print(f"❌ Path not found: {path}")
    except Exception as e:
        print(f"Error opening path: {e}")

def set_brightness(level):
    try:
        sbc.set_brightness(level)
    except Exception as e:
        print(f"Error setting brightness: {e}")

def execute_command(cmd_json):
    if not cmd_json: return
    action = cmd_json.get("action")
    
    if action == "take_screenshot": return capture_screen() 
    elif action == "camera_stream" or action == "camera_snap": return capture_webcam()
    elif action == "check_battery": return get_battery_status()
    elif action == "check_health": return get_system_health()
    elif action == "system_sleep": system_sleep()
    elif action == "record_audio": 
        duration = cmd_json.get("duration", 10)
        return record_audio(duration)
    
   
    elif action == "open_url": 
        open_browser(cmd_json.get("url"), cmd_json.get("browser", "default"))
        
    elif action == "close_app": close_application(cmd_json.get("app_name"))
    elif action == "open_app":
        app_name = cmd_json.get("app_name")
        print(f"🚀 Launching {app_name}...")
        pyautogui.press("win")
        pyautogui.sleep(0.1)
        pyautogui.write(app_name)
        pyautogui.sleep(0.5)
        pyautogui.press("enter")
    elif action == "system_control":
        feature = cmd_json.get("feature")
        val = cmd_json.get("value")
        if feature == "brightness": set_brightness(val)
    elif action == "open_file": open_file_path(cmd_json.get("path"))