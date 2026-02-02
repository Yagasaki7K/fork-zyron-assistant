# 🔌 Browser Extension Installation Guide

## Overview
The **Pikachu Activity Monitor** extension allows your assistant to see all open browser tabs with their URLs. This greatly enhances the `/activities` command functionality.

---

## 📦 Installation Steps

### **For Google Chrome / Brave / Edge (Chromium-based browsers)**

1. **Locate the Extension Folder**
   - The extension files are in: `browser_extension/`
   - Contains: `manifest.json`, `background.js`, `popup.html`, `popup.js`, and icon files

2. **Open Extension Management**
   - **Chrome**: Navigate to `chrome://extensions/`
   - **Brave**: Navigate to `brave://extensions/`
   - **Edge**: Navigate to `edge://extensions/`

3. **Enable Developer Mode**
   - Look for "Developer mode" toggle in the top-right corner
   - Turn it **ON**

4. **Load the Extension**
   - Click **"Load unpacked"** button
   - Browse to your project folder and select the `browser_extension` folder
   - Click **"Select Folder"**

5. **Verify Installation**
   - You should see "Pikachu Activity Monitor" in your extensions list
   - The extension icon should appear in your browser toolbar
   - Status should show "Active"

6. **Pin the Extension (Optional)**
   - Click the puzzle piece icon in your toolbar
   - Find "Pikachu Activity Monitor"
   - Click the pin icon to keep it visible

---

## ✅ Testing the Extension

### **Method 1: Using the Popup**
1. Click the Pikachu extension icon in your toolbar
2. You should see:
   - Total tab count
   - Number of windows
   - List of all open tabs with titles and URLs

### **Method 2: Using Telegram Bot**
1. Open Telegram and message your bot
2. Send: `/activities` or `/current_activities`
3. You should receive a detailed report including:
   - All browser tabs with URLs
   - Desktop applications
   - System status

### **Method 3: Using Voice Command**
1. Say "Hey Pikachu"
2. Say "Show me current activities" or "What's open?"
3. Pikachu will speak the summary

---

## 🔧 How It Works

### **Extension Architecture**
```
Browser Extension (JavaScript)
        ↓
   Monitors Tabs
        ↓
Activity Monitor (Python)
        ↓
  Formats Data
        ↓
Pikachu Assistant → User
```

### **What Data is Collected?**
- Tab titles
- Tab URLs
- Window information
- Active/inactive status

### **Privacy & Security**
- ✅ All data stays LOCAL on your computer
- ✅ No data is sent to external servers
- ✅ Only accessible by YOUR Pikachu assistant
- ✅ Extension has NO internet permissions

---

## 🐛 Troubleshooting

### **Extension Not Showing Tabs**
**Problem**: `/activities` shows "No tabs detected"

**Solutions**:
1. Make sure the extension is **enabled** in `chrome://extensions/`
2. Check if "Developer mode" is still ON
3. Reload the extension:
   - Go to `chrome://extensions/`
   - Find "Pikachu Activity Monitor"
   - Click the reload icon (🔄)
4. Refresh your open tabs

### **Extension Shows as "Errors"**
**Problem**: Red "Errors" badge on extension

**Solutions**:
1. Click "Errors" to see details
2. Common fixes:
   - Make sure all files are in the `browser_extension` folder
   - Check file permissions
   - Reload the extension
3. If persistent, try:
   - Remove extension
   - Restart browser
   - Re-install using steps above

### **Can't Find Extension Icon**
**Problem**: Extension installed but icon not visible

**Solutions**:
1. Click the puzzle piece (🧩) icon in toolbar
2. Look for "Pikachu Activity Monitor"
3. Click the pin icon to make it permanently visible

### **Tabs Not Updating**
**Problem**: Old tabs still showing

**Solutions**:
1. Click the extension icon
2. Press the "🔄 Refresh Tabs" button
3. Or run `/activities` command again

---

## 🌐 Multi-Browser Support

### **Running on Multiple Browsers**
You can install the extension on:
- ✅ Google Chrome
- ✅ Brave
- ✅ Microsoft Edge
- ✅ Any Chromium-based browser

**Note**: Install separately on each browser you use.

### **Firefox Support**
The current extension uses Manifest V3 (Chrome format).
For Firefox, you would need a WebExtensions version (planned for future update).

---

## 📊 Features Enabled

With the extension installed, you get:

### **Detailed Browser Activity**
```
🌐 BROWSERS:

▫️ Google Chrome
   1. YouTube - Watch videos
      🔗 https://www.youtube.com/watch?v=...
   2. Gmail - Inbox
      🔗 https://mail.google.com/mail/u/0/
   3. GitHub - Repository
      🔗 https://github.com/user/repo

▫️ Brave Browser
   1. Documentation
      🔗 https://docs.example.com
```

### **Without Extension**
```
🌐 BROWSERS:

▫️ Google Chrome
   (No tabs detected - Install extension for full details)
```

---

## 🔄 Updating the Extension

If you make changes to extension files:

1. Go to `chrome://extensions/`
2. Find "Pikachu Activity Monitor"
3. Click the reload icon (🔄)
4. Changes will take effect immediately

---

## 🗑️ Uninstalling

To remove the extension:

1. Go to `chrome://extensions/`
2. Find "Pikachu Activity Monitor"
3. Click **"Remove"**
4. Confirm deletion

**Note**: This only removes browser access. The assistant will still work but won't show browser URLs.

---

## 💡 Tips

1. **Keep Extension Updated**: If you update Pikachu, check for extension updates too
2. **Multiple Profiles**: Install separately for each Chrome profile
3. **Incognito Mode**: Won't work in incognito unless you explicitly allow it
4. **Performance**: Minimal impact - only reads data when requested

---

## 🆘 Still Need Help?

If you encounter issues:

1. Check the browser console (F12 → Console tab)
2. Look for errors related to "Pikachu Activity Monitor"
3. Try reinstalling the extension
4. Ensure `activity_monitor.py` is in your project folder

---

**Extension Status Check Command**:
```
Send to bot: /activities

If you see detailed URLs → ✅ Working perfectly
If you see "Install extension" → ⚠️ Extension not installed or not working
```

