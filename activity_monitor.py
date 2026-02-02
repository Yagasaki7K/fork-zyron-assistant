"""
Activity Monitor Module for Pikachu Desktop Assistant
Monitors running applications, browser tabs, and system processes
"""

import psutil
import json
import os
import subprocess
from collections import defaultdict

# Browser executable names
BROWSER_PROCESSES = {
    'chrome.exe': 'Google Chrome',
    'msedge.exe': 'Microsoft Edge',
    'brave.exe': 'Brave Browser',
    'firefox.exe': 'Mozilla Firefox',
    'opera.exe': 'Opera'
}

def get_running_processes():
    """Get all running processes with their details"""
    processes = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'exe': proc.info['exe'],
                    'cmdline': proc.info['cmdline']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as e:
        print(f"Error getting processes: {e}")
    
    return processes


def get_chrome_tabs_from_extension():
    """
    Attempt to get Chrome tabs from the extension via local storage file
    This is a fallback method - the extension should be running
    """
    tabs = []
    
    try:
        # Try to read Chrome's session data
        # This is a simplified approach - the extension method is preferred
        chrome_data_path = os.path.join(
            os.environ.get('LOCALAPPDATA', ''),
            'Google', 'Chrome', 'User Data', 'Default'
        )
        
        # Check if a tabs data file exists (created by our extension)
        tabs_file = os.path.join(chrome_data_path, 'pikachu_tabs.json')
        
        if os.path.exists(tabs_file):
            with open(tabs_file, 'r', encoding='utf-8') as f:
                tabs = json.load(f)
    except Exception as e:
        print(f"Could not read Chrome tabs from extension: {e}")
    
    return tabs


def get_browser_tabs_windows():
    """
    Get browser tabs using Windows COM automation
    Works for Chrome-based browsers
    """
    tabs_by_browser = defaultdict(list)
    
    try:
        # For Chrome-based browsers, we'll use a PowerShell approach
        # This gets the window titles which often contain the page title
        powershell_cmd = """
        Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | 
        Select-Object ProcessName, MainWindowTitle | 
        ConvertTo-Json
        """
        
        result = subprocess.run(
            ['powershell', '-Command', powershell_cmd],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and result.stdout:
            windows = json.loads(result.stdout)
            
            # Ensure it's a list
            if not isinstance(windows, list):
                windows = [windows]
            
            for window in windows:
                proc_name = window.get('ProcessName', '').lower()
                title = window.get('MainWindowTitle', '')
                
                if proc_name in ['chrome', 'msedge', 'brave', 'firefox']:
                    browser_name = BROWSER_PROCESSES.get(f"{proc_name}.exe", proc_name.title())
                    
                    # Extract URL from title if possible (many browsers show it)
                    # Format is usually: "Page Title - Browser Name"
                    if title and title not in ['', browser_name]:
                        tabs_by_browser[browser_name].append({
                            'title': title,
                            'url': 'N/A (Install extension for URLs)'
                        })
    
    except Exception as e:
        print(f"Error getting browser windows: {e}")
    
    return dict(tabs_by_browser)


def get_desktop_applications():
    """Get list of desktop applications currently running"""
    apps = []
    
    # Common desktop applications
    desktop_apps = {
        'notepad.exe': 'Notepad',
        'Code.exe': 'Visual Studio Code',
        'EXCEL.EXE': 'Microsoft Excel',
        'WINWORD.EXE': 'Microsoft Word',
        'POWERPNT.EXE': 'Microsoft PowerPoint',
        'spotify.exe': 'Spotify',
        'Discord.exe': 'Discord',
        'Telegram.exe': 'Telegram',
        'WhatsApp.exe': 'WhatsApp',
        'Zoom.exe': 'Zoom',
        'Teams.exe': 'Microsoft Teams',
        'slack.exe': 'Slack',
        'vlc.exe': 'VLC Media Player',
        'explorer.exe': 'File Explorer',
        'notepad++.exe': 'Notepad++',
        'sublime_text.exe': 'Sublime Text',
        'pycharm64.exe': 'PyCharm',
        'idea64.exe': 'IntelliJ IDEA',
        'studio64.exe': 'Android Studio',
        'photoshop.exe': 'Adobe Photoshop',
        'illustrator.exe': 'Adobe Illustrator',
        'Figma.exe': 'Figma',
        'gimp.exe': 'GIMP',
        'obs64.exe': 'OBS Studio',
        'steamwebhelper.exe': 'Steam',
    }
    
    processes = get_running_processes()
    found_apps = set()
    
    for proc in processes:
        proc_name = proc['name']
        
        # Check if it's a browser (we'll handle browsers separately)
        if proc_name in BROWSER_PROCESSES:
            continue
        
        # Check if it's a known desktop app
        if proc_name in desktop_apps:
            app_name = desktop_apps[proc_name]
            if app_name not in found_apps:
                apps.append({
                    'name': app_name,
                    'process': proc_name,
                    'pid': proc['pid']
                })
                found_apps.add(app_name)
    
    # Sort alphabetically
    apps.sort(key=lambda x: x['name'])
    
    return apps


def get_current_activities():
    """
    Main function to get all current activities
    Returns a structured dictionary with browsers, desktop apps, and system info
    """
    
    print("🔍 Collecting current activities...")
    
    activities = {
        'browsers': {},
        'desktop_apps': [],
        'system_info': {}
    }
    
    # Get browser tabs
    print("   → Checking browsers...")
    browser_tabs = get_browser_tabs_windows()
    
    # Also check which browsers are running
    processes = get_running_processes()
    running_browsers = []
    
    for proc in processes:
        if proc['name'] in BROWSER_PROCESSES:
            browser_name = BROWSER_PROCESSES[proc['name']]
            if browser_name not in running_browsers:
                running_browsers.append(browser_name)
                
                # Initialize browser entry if not exists
                if browser_name not in activities['browsers']:
                    activities['browsers'][browser_name] = []
    
    # Merge the tab data
    for browser, tabs in browser_tabs.items():
        if browser in activities['browsers']:
            activities['browsers'][browser].extend(tabs)
        else:
            activities['browsers'][browser] = tabs
    
    # Get desktop applications
    print("   → Checking desktop applications...")
    activities['desktop_apps'] = get_desktop_applications()
    
    # Add system info
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        
        activities['system_info'] = {
            'cpu_usage': f"{cpu_percent}%",
            'ram_usage': f"{mem.percent}%",
            'ram_available': f"{round(mem.available / (1024**3), 2)} GB",
            'total_processes': len(list(psutil.process_iter()))
        }
    except Exception as e:
        print(f"Error getting system info: {e}")
    
    print("✅ Activity collection complete!")
    return activities


def format_activities_text(activities):
    """Format activities into a readable text format for Telegram"""
    
    lines = ["📊 **CURRENT ACTIVITIES**\n"]
    
    # Browsers Section
    if activities['browsers']:
        lines.append("🌐 **BROWSERS:**")
        for browser, tabs in activities['browsers'].items():
            lines.append(f"\n▫️ **{browser}**")
            if tabs:
                for i, tab in enumerate(tabs, 1):
                    title = tab.get('title', 'Unknown')
                    url = tab.get('url', 'N/A')
                    
                    # Truncate long titles
                    if len(title) > 60:
                        title = title[:57] + "..."
                    
                    if url == 'N/A (Install extension for URLs)':
                        lines.append(f"   {i}. {title}")
                    else:
                        lines.append(f"   {i}. {title}")
                        lines.append(f"      🔗 {url}")
            else:
                lines.append("   (No tabs detected - Install extension for full details)")
        lines.append("")
    
    # Desktop Applications
    if activities['desktop_apps']:
        lines.append("🖥️ **DESKTOP APPLICATIONS:**")
        for app in activities['desktop_apps']:
            lines.append(f"   • {app['name']}")
        lines.append("")
    
    # System Info
    if activities['system_info']:
        info = activities['system_info']
        lines.append("⚙️ **SYSTEM STATUS:**")
        lines.append(f"   CPU: {info.get('cpu_usage', 'N/A')}")
        lines.append(f"   RAM: {info.get('ram_usage', 'N/A')} (Free: {info.get('ram_available', 'N/A')})")
        lines.append(f"   Processes: {info.get('total_processes', 'N/A')}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Test the module
    activities = get_current_activities()
    print("\n" + "="*60)
    print(format_activities_text(activities))
    print("="*60)