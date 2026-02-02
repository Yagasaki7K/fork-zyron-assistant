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
import requests
import json
import activity_monitor  

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

def get_laptop_location():
    """
    Gets the approximate location of the laptop using multiple IP geolocation services
    for better accuracy. Tries 3 different APIs and returns the best result.
    """
    try:
        print("📍 Fetching location from multiple sources...")
        
        results = []
        
        try:
            print("   → Checking ipapi.co...")
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                results.append({
                    'source': 'ipapi.co',
                    'ip': data.get('ip', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('region', 'Unknown'),
                    'country': data.get('country_name', 'Unknown'),
                    'country_code': data.get('country_code', 'Unknown'),
                    'postal': data.get('postal', 'Unknown'),
                    'latitude': data.get('latitude', 0),
                    'longitude': data.get('longitude', 0),
                    'timezone': data.get('timezone', 'Unknown'),
                    'org': data.get('org', 'Unknown'),
                })
                print(f"      ✓ Found: {data.get('city', 'Unknown')}")
        except Exception as e:
            print(f"      ✗ ipapi.co failed: {e}")
        
        try:
            print("   → Checking ip-api.com...")
            response = requests.get('http://ip-api.com/json/?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    results.append({
                        'source': 'ip-api.com',
                        'ip': data.get('query', 'Unknown'),
                        'city': data.get('city', 'Unknown'),
                        'region': data.get('regionName', 'Unknown'),
                        'country': data.get('country', 'Unknown'),
                        'country_code': data.get('countryCode', 'Unknown'),
                        'postal': data.get('zip', 'Unknown'),
                        'latitude': data.get('lat', 0),
                        'longitude': data.get('lon', 0),
                        'timezone': data.get('timezone', 'Unknown'),
                        'org': data.get('isp', 'Unknown'),
                    })
                    print(f"      ✓ Found: {data.get('city', 'Unknown')}")
        except Exception as e:
            print(f"      ✗ ip-api.com failed: {e}")
        
        try:
            print("   → Checking ipinfo.io...")
            response = requests.get('https://ipinfo.io/json', timeout=5)
            if response.status_code == 200:
                data = response.json()
                loc = data.get('loc', '0,0').split(',')
                results.append({
                    'source': 'ipinfo.io',
                    'ip': data.get('ip', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('region', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'country_code': data.get('country', 'Unknown'),
                    'postal': data.get('postal', 'Unknown'),
                    'latitude': float(loc[0]) if len(loc) > 0 else 0,
                    'longitude': float(loc[1]) if len(loc) > 1 else 0,
                    'timezone': data.get('timezone', 'Unknown'),
                    'org': data.get('org', 'Unknown'),
                })
                print(f"      ✓ Found: {data.get('city', 'Unknown')}")
        except Exception as e:
            print(f"      ✗ ipinfo.io failed: {e}")
        
        if not results:
            print("❌ All location APIs failed")
            return None
        
        best_result = None
        for result in results:
            if result['source'] == 'ip-api.com':  
                best_result = result
                break
        
        if not best_result:
            best_result = results[0] 
        
       
        if len(results) > 1:
            comparison = "\n".join([f"   • {r['source']}: {r['city']}, {r['region']}" for r in results])
            best_result['comparison'] = comparison
        else:
            best_result['comparison'] = None
        
       
        lat = best_result['latitude']
        lon = best_result['longitude']
        best_result['maps_url'] = f"https://www.google.com/maps?q={lat},{lon}"
        
        print(f"✅ Best location: {best_result['city']}, {best_result['region']} (from {best_result['source']})")
        return best_result
            
    except Exception as e:
        print(f"❌ Error getting location: {e}")
        return None


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
    SAMPLE_RATE = 44100 
    CHANNELS = 1 
    
    print(f"🎤 Recording audio for {duration} seconds...")
    
    try:
     
        recording = sd.rec(
            int(duration * SAMPLE_RATE), 
            samplerate=SAMPLE_RATE, 
            channels=CHANNELS, 
            dtype='int16'
        )
      
        sd.wait()
        
        print("✅ Recording complete.")
        
       
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
    elif action == "get_location": return get_laptop_location() 
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

    elif action == "get_activities":
        return activity_monitor.get_current_activities()