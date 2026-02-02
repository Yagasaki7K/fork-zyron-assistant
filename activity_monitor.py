"""
Activity Monitor Module for Pikachu Desktop Assistant
Monitors running applications, browser tabs, and system processes
"""

import psutil
import json
import os
import subprocess
import sqlite3
import shutil
from collections import defaultdict
from pathlib import Path

try:
    import win32gui
    import win32process
    import win32con
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False
    print("Warning: pywin32 not available. Tab detection will use fallback method.")

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


def get_chrome_tabs():
    """Get all Chrome tabs from session storage"""
    tabs = []
    
    try:
        # Chrome user data path
        chrome_path = os.path.join(
            os.environ.get('LOCALAPPDATA', ''),
            'Google', 'Chrome', 'User Data', 'Default'
        )
        
        # Try to read from Sessions directory
        sessions_path = os.path.join(chrome_path, 'Sessions')
        current_session = os.path.join(sessions_path, 'Session_13131313131313')
        tabs_file = os.path.join(sessions_path, 'Tabs_13131313131313')
        
        # Try reading the session database
        session_db = None
        for file in ['Current Session', 'Current Tabs']:
            db_path = os.path.join(chrome_path, file)
            if os.path.exists(db_path):
                session_db = db_path
                break
        
        # Try History database as fallback
        history_db = os.path.join(chrome_path, 'History')
        
        if os.path.exists(history_db):
            # Copy to temp location to avoid lock
            temp_db = os.path.join(os.environ.get('TEMP', ''), 'chrome_history_temp.db')
            try:
                shutil.copy2(history_db, temp_db)
                
                conn = sqlite3.connect(temp_db)
                cursor = conn.cursor()
                
                # Get recent URLs (likely open tabs)
                cursor.execute("""
                    SELECT url, title, last_visit_time 
                    FROM urls 
                    ORDER BY last_visit_time DESC 
                    LIMIT 100
                """)
                
                results = cursor.fetchall()
                conn.close()
                
                # Clean up temp file
                try:
                    os.remove(temp_db)
                except:
                    pass
                
                # Return top results as likely open tabs
                for url, title, _ in results[:30]:  # Limit to 30 most recent
                    if url and title:
                        tabs.append({
                            'title': title,
                            'url': url
                        })
                        
            except Exception as e:
                print(f"Error reading Chrome history: {e}")
                
    except Exception as e:
        print(f"Error getting Chrome tabs: {e}")
    
    return tabs


def get_brave_tabs():
    """Get all Brave tabs from session storage"""
    tabs = []
    
    try:
        # Brave user data path
        brave_path = os.path.join(
            os.environ.get('LOCALAPPDATA', ''),
            'BraveSoftware', 'Brave-Browser', 'User Data', 'Default'
        )
        
        history_db = os.path.join(brave_path, 'History')
        
        if os.path.exists(history_db):
            temp_db = os.path.join(os.environ.get('TEMP', ''), 'brave_history_temp.db')
            try:
                shutil.copy2(history_db, temp_db)
                
                conn = sqlite3.connect(temp_db)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT url, title, last_visit_time 
                    FROM urls 
                    ORDER BY last_visit_time DESC 
                    LIMIT 100
                """)
                
                results = cursor.fetchall()
                conn.close()
                
                try:
                    os.remove(temp_db)
                except:
                    pass
                
                for url, title, _ in results[:30]:
                    if url and title:
                        tabs.append({
                            'title': title,
                            'url': url
                        })
                        
            except Exception as e:
                print(f"Error reading Brave history: {e}")
                
    except Exception as e:
        print(f"Error getting Brave tabs: {e}")
    
    return tabs


def get_edge_tabs():
    """Get all Edge tabs from session storage"""
    tabs = []
    
    try:
        # Edge user data path
        edge_path = os.path.join(
            os.environ.get('LOCALAPPDATA', ''),
            'Microsoft', 'Edge', 'User Data', 'Default'
        )
        
        history_db = os.path.join(edge_path, 'History')
        
        if os.path.exists(history_db):
            temp_db = os.path.join(os.environ.get('TEMP', ''), 'edge_history_temp.db')
            try:
                shutil.copy2(history_db, temp_db)
                
                conn = sqlite3.connect(temp_db)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT url, title, last_visit_time 
                    FROM urls 
                    ORDER BY last_visit_time DESC 
                    LIMIT 100
                """)
                
                results = cursor.fetchall()
                conn.close()
                
                try:
                    os.remove(temp_db)
                except:
                    pass
                
                for url, title, _ in results[:30]:
                    if url and title:
                        tabs.append({
                            'title': title,
                            'url': url
                        })
                        
            except Exception as e:
                print(f"Error reading Edge history: {e}")
                
    except Exception as e:
        print(f"Error getting Edge tabs: {e}")
    
    return tabs


def get_firefox_tabs():
    """Get Firefox tabs using PowerShell and Places database"""
    tabs = []
    
    try:
        # Firefox profile path
        firefox_path = os.path.join(
            os.environ.get('APPDATA', ''),
            'Mozilla', 'Firefox', 'Profiles'
        )
        
        if not os.path.exists(firefox_path):
            return tabs
        
        # Find default profile
        profiles = [d for d in os.listdir(firefox_path) if os.path.isdir(os.path.join(firefox_path, d))]
        
        for profile in profiles:
            if 'default' in profile.lower() or 'release' in profile.lower():
                profile_path = os.path.join(firefox_path, profile)
                places_db = os.path.join(profile_path, 'places.sqlite')
                
                if os.path.exists(places_db):
                    temp_db = os.path.join(os.environ.get('TEMP', ''), 'firefox_places_temp.db')
                    try:
                        shutil.copy2(places_db, temp_db)
                        
                        conn = sqlite3.connect(temp_db)
                        cursor = conn.cursor()
                        
                        cursor.execute("""
                            SELECT url, title, last_visit_date 
                            FROM moz_places 
                            WHERE title IS NOT NULL 
                            ORDER BY last_visit_date DESC 
                            LIMIT 50
                        """)
                        
                        results = cursor.fetchall()
                        conn.close()
                        
                        try:
                            os.remove(temp_db)
                        except:
                            pass
                        
                        for url, title, _ in results[:30]:
                            if url and title:
                                tabs.append({
                                    'title': title,
                                    'url': url
                                })
                        
                        break  # Found default profile, exit loop
                        
                    except Exception as e:
                        print(f"Error reading Firefox places: {e}")
                        
    except Exception as e:
        print(f"Error getting Firefox tabs: {e}")
    
    return tabs


def get_browser_tabs_win32():
    """Get browser tabs using win32gui - reads ACTUAL open windows only"""
    if not HAS_WIN32:
        return None
    
    tabs_by_browser = defaultdict(list)
    
    def get_process_name(hwnd):
        """Get process name for a window"""
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['pid'] == pid:
                    return proc.info['name']
        except:
            pass
        return None
    
    def enum_windows_callback(hwnd, _):
        """Callback for enumerating windows"""
        if win32gui.IsWindowVisible(hwnd):
            try:
                proc_name = get_process_name(hwnd)
                
                if proc_name and proc_name in BROWSER_PROCESSES:
                    title = win32gui.GetWindowText(hwnd)
                    
                    if title and title.strip():
                        browser_name = BROWSER_PROCESSES[proc_name]
                        
                        # Clean up the title (remove browser name suffix)
                        for suffix in [f' - {browser_name}', f' — {browser_name}', 
                                      ' - Google Chrome', ' - Brave', ' - Microsoft Edge',
                                      ' - Mozilla Firefox', ' - Chromium']:
                            if title.endswith(suffix):
                                title = title[:-len(suffix)]
                                break
                        
                        # Skip generic/empty titles
                        if title.strip() and title not in ['New Tab', 'Chrome', 'Brave', 'Edge', 'Firefox']:
                            tabs_by_browser[browser_name].append({
                                'title': title.strip(),
                                'url': 'Install extension for URLs'
                            })
            except Exception as e:
                pass
    
    try:
        win32gui.EnumWindows(enum_windows_callback, None)
    except Exception as e:
        print(f"Error enumerating windows: {e}")
    
    return dict(tabs_by_browser)


def get_browser_tabs_all():
    """Get browser tabs from all detected browsers using their databases"""
    
    # First try win32 method if available (gets actual open windows)
    if HAS_WIN32:
        print("   → Using win32 method for actual open tabs...")
        win32_tabs = get_browser_tabs_win32()
        if win32_tabs:
            # Enhance with URLs from history database
            processes = get_running_processes()
            running_browsers = set()
            
            for proc in processes:
                if proc['name'] in BROWSER_PROCESSES:
                    browser_name = BROWSER_PROCESSES[proc['name']]
                    running_browsers.add(browser_name)
            
            print(f"   → Detected running browsers: {running_browsers}")
            
            # Try to get URLs from history for each browser
            for browser_name in win32_tabs.keys():
                if browser_name == 'Google Chrome':
                    chrome_tabs = get_chrome_tabs()
                    # Match titles and add URLs
                    for tab in win32_tabs[browser_name]:
                        for history_tab in chrome_tabs:
                            if history_tab['title'] == tab['title']:
                                tab['url'] = history_tab['url']
                                break
                
                elif browser_name == 'Brave Browser':
                    brave_tabs = get_brave_tabs()
                    for tab in win32_tabs[browser_name]:
                        for history_tab in brave_tabs:
                            if history_tab['title'] == tab['title']:
                                tab['url'] = history_tab['url']
                                break
                
                elif browser_name == 'Microsoft Edge':
                    edge_tabs = get_edge_tabs()
                    for tab in win32_tabs[browser_name]:
                        for history_tab in edge_tabs:
                            if history_tab['title'] == tab['title']:
                                tab['url'] = history_tab['url']
                                break
                
                elif browser_name == 'Mozilla Firefox':
                    firefox_tabs = get_firefox_tabs()
                    for tab in win32_tabs[browser_name]:
                        for history_tab in firefox_tabs:
                            if history_tab['title'] == tab['title']:
                                tab['url'] = history_tab['url']
                                break
            
            return win32_tabs
    
    # Fallback to database method if win32 not available
    tabs_by_browser = defaultdict(list)
    
    # Get running processes to see which browsers are active
    processes = get_running_processes()
    running_browsers = set()
    
    for proc in processes:
        if proc['name'] in BROWSER_PROCESSES:
            browser_name = BROWSER_PROCESSES[proc['name']]
            running_browsers.add(browser_name)
    
    print(f"   → Detected running browsers: {running_browsers}")
    
    # Get tabs for each running browser
    if 'Google Chrome' in running_browsers:
        print("   → Fetching Chrome tabs...")
        chrome_tabs = get_chrome_tabs()
        if chrome_tabs:
            tabs_by_browser['Google Chrome'] = chrome_tabs
            print(f"      ✓ Found {len(chrome_tabs)} Chrome tabs")
    
    if 'Brave Browser' in running_browsers:
        print("   → Fetching Brave tabs...")
        brave_tabs = get_brave_tabs()
        if brave_tabs:
            tabs_by_browser['Brave Browser'] = brave_tabs
            print(f"      ✓ Found {len(brave_tabs)} Brave tabs")
    
    if 'Microsoft Edge' in running_browsers:
        print("   → Fetching Edge tabs...")
        edge_tabs = get_edge_tabs()
        if edge_tabs:
            tabs_by_browser['Microsoft Edge'] = edge_tabs
            print(f"      ✓ Found {len(edge_tabs)} Edge tabs")
    
    if 'Mozilla Firefox' in running_browsers:
        print("   → Fetching Firefox tabs...")
        firefox_tabs = get_firefox_tabs()
        if firefox_tabs:
            tabs_by_browser['Mozilla Firefox'] = firefox_tabs
            print(f"      ✓ Found {len(firefox_tabs)} Firefox tabs")
    
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
    
    # Get browser tabs using database method
    print("   → Checking browsers...")
    browser_tabs = get_browser_tabs_all()
    activities['browsers'] = browser_tabs
    
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


def format_activities_text(activities, max_message_length=4000):
    """
    Format activities into a readable text format for Telegram
    Handles message length limits by splitting into multiple parts if needed
    Returns either a single string or a list of strings
    """
    
    lines = ["📊 **CURRENT ACTIVITIES**\n"]
    
    # Browsers Section
    if activities['browsers']:
        lines.append("🌐 **BROWSERS:**")
        for browser, tabs in activities['browsers'].items():
            lines.append(f"\n▫️ **{browser}** ({len(tabs)} tabs)")
            if tabs:
                for i, tab in enumerate(tabs, 1):
                    title = tab.get('title', 'Unknown')
                    url = tab.get('url', 'N/A')
                    
                    # Truncate long titles
                    if len(title) > 60:
                        title = title[:57] + "..."
                    
                    lines.append(f"   {i}. {title}")
                    
                    # Only show URL if it's not the placeholder
                    if url and url != 'Install extension for URLs':
                        if len(url) > 100:
                            url = url[:97] + "..."
                        lines.append(f"      🔗 {url}")
            else:
                lines.append("   (No tabs detected)")
        lines.append("")
    else:
        lines.append("🌐 **BROWSERS:**")
        lines.append("   (No browsers running)\n")
    
    # Desktop Applications
    if activities['desktop_apps']:
        lines.append("🖥️ **DESKTOP APPLICATIONS:**")
        for app in activities['desktop_apps']:
            lines.append(f"   • {app['name']}")
        lines.append("")
    else:
        lines.append("🖥️ **DESKTOP APPLICATIONS:**")
        lines.append("   (No major applications detected)\n")
    
    # System Info
    if activities['system_info']:
        info = activities['system_info']
        lines.append("⚙️ **SYSTEM STATUS:**")
        lines.append(f"   CPU: {info.get('cpu_usage', 'N/A')}")
        lines.append(f"   RAM: {info.get('ram_usage', 'N/A')} (Free: {info.get('ram_available', 'N/A')})")
        lines.append(f"   Processes: {info.get('total_processes', 'N/A')}")
    
    full_text = "\n".join(lines)
    
    # Check if message is too long
    if len(full_text) > max_message_length:
        print(f"   ⚠️ Message too long ({len(full_text)} chars), splitting...")
        return split_long_message(activities, max_message_length)
    
    return full_text


def split_long_message(activities, max_length=4000):
    """
    Split activities into multiple messages if too long
    Returns a list of message strings
    """
    messages = []
    
    # Message 1: Header + Browser Summary
    lines = ["📊 **CURRENT ACTIVITIES**\n"]
    lines.append("🌐 **BROWSERS:**")
    
    if activities['browsers']:
        total_tabs = sum(len(tabs) for tabs in activities['browsers'].values())
        lines.append(f"Total: {total_tabs} tabs across {len(activities['browsers'])} browsers\n")
        
        for browser, tabs in activities['browsers'].items():
            lines.append(f"▫️ **{browser}**: {len(tabs)} tabs")
        
        messages.append("\n".join(lines))
        
        # Message 2+: Detailed tabs for each browser
        for browser, tabs in activities['browsers'].items():
            if tabs:
                browser_lines = [f"\n🌐 **{browser} Details:**\n"]
                current_batch = []
                
                for i, tab in enumerate(tabs, 1):
                    title = tab.get('title', 'Unknown')
                    url = tab.get('url', 'N/A')
                    
                    if len(title) > 70:
                        title = title[:67] + "..."
                    
                    tab_line = f"{i}. {title}"
                    current_batch.append(tab_line)
                    
                    # Only add URL if available
                    if url and url != 'Install extension for URLs':
                        if len(url) > 90:
                            url = url[:87] + "..."
                        current_batch.append(f"   🔗 {url}")
                    
                    # Check if we're approaching limit
                    test_text = "\n".join(browser_lines + current_batch)
                    if len(test_text) > max_length - 300:
                        # Send current batch
                        messages.append("\n".join(browser_lines + current_batch))
                        browser_lines = [f"\n🌐 **{browser} (continued):**\n"]
                        current_batch = []
                
                # Add remaining lines
                if current_batch:
                    messages.append("\n".join(browser_lines + current_batch))
    else:
        lines.append("   (No browsers running)")
        messages.append("\n".join(lines))
    
    # Final message: Apps + System Status
    final_lines = []
    
    if activities['desktop_apps']:
        final_lines.append("\n🖥️ **DESKTOP APPLICATIONS:**")
        for app in activities['desktop_apps']:
            final_lines.append(f"   • {app['name']}")
        final_lines.append("")
    
    if activities['system_info']:
        info = activities['system_info']
        final_lines.append("⚙️ **SYSTEM STATUS:**")
        final_lines.append(f"   CPU: {info.get('cpu_usage', 'N/A')}")
        final_lines.append(f"   RAM: {info.get('ram_usage', 'N/A')} (Free: {info.get('ram_available', 'N/A')})")
        final_lines.append(f"   Processes: {info.get('total_processes', 'N/A')}")
    
    if final_lines:
        messages.append("\n".join(final_lines))
    
    return messages


if __name__ == "__main__":
    # Test the module
    activities = get_current_activities()
    print("\n" + "="*60)
    result = format_activities_text(activities)
    
    if isinstance(result, list):
        for i, msg in enumerate(result, 1):
            print(f"\n--- MESSAGE {i} ---")
            print(msg)
            print("="*60)
    else:
        print(result)
        print("="*60)