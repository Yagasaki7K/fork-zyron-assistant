# Zyron Desktop Assistant

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6.svg?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![AI Engine](https://img.shields.io/badge/AI-Ollama-000000.svg?style=for-the-badge&logo=ai&logoColor=white)](https://ollama.com)
[![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local-00C853.svg?style=for-the-badge&logo=shield&logoColor=white)](#)
[![License](https://img.shields.io/badge/License-MIT-FFC107.svg?style=for-the-badge&logo=open-source-initiative&logoColor=white)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.2-4CAF50.svg?style=for-the-badge)](CHANGELOG.md)

**Intelligent Desktop Automation with Privacy-First Architecture**

*Local AI Processing • Zero Cloud Dependencies • Enterprise-Grade Security*

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Configuration](#configuration) • [Documentation](#faq)

</div>

---

## Overview

Zyron Desktop Assistant is a sophisticated automation platform that transforms Windows workstations into intelligent, voice-controlled environments. Built on a privacy-first architecture, the system operates entirely offline using Ollama's local inference engine—eliminating external API dependencies and ensuring complete data sovereignty.

### Core Value Proposition

**Privacy & Security**
- All processing occurs on-device using local AI inference
- Zero telemetry or cloud service integration
- Bank-grade security with no external data transmission

**Dual Control Interface**
- Voice activation with customizable wake word detection
- Remote management via encrypted Telegram integration

**Cost Efficiency**
- No subscription fees or API usage costs
- Open-source foundation with extensible architecture

**Production Ready**
- Python-based implementation for easy customization
- Comprehensive logging and error handling
- Auto-start capabilities with stealth operation mode

---

## Features

### System Capabilities

**Voice Recognition & Control**
- Wake word detection with configurable activation phrase
- Natural language processing via Qwen 2.5 Coder (7B parameter model)
- Hands-free operation for accessibility and convenience

**Remote Management**
- Telegram bot integration for remote system access
- Secure command execution from any location
- Real-time status updates and notifications

**System Automation**
- Application lifecycle management (launch, terminate, monitor)
- System power management (sleep, shutdown, restart, lock)
- Screenshot and webcam capture capabilities
- File system navigation and management

**Health & Monitoring**
- Real-time resource utilization tracking (CPU, RAM, Disk)
- Battery status monitoring with charge level reporting
- Activity tracking for running applications and browser sessions
- IP-based geolocation services

**Media Capabilities**
- 10-second audio recording with dual-source capture (system + microphone)
- Visual monitoring through screenshot and webcam integration
- Automated media processing and delivery via Telegram

### Command Examples

**System Management**
```plaintext
Open Chrome                 → Launch specified application
Take a screenshot          → Capture current screen state
System status              → Comprehensive health report
Sleep                      → Initiate system sleep mode
List my documents          → Directory listing with file details
```

**Monitoring & Intelligence**
```plaintext
Record audio               → 10-second dual-source audio capture
Show activities            → Active applications and browser tabs
Location                   → IP-based geolocation query
```

**Voice Activation**
```plaintext
Hey Zyron, open Spotify
Hey Zyron, what's my battery level?
Hey Zyron, take a screenshot
Hey Zyron, what am I doing?
Hey Zyron, where am I?
```

---

## System Requirements

| Component | Specification | Source |
|-----------|---------------|--------|
| **Operating System** | Windows 10/11 (64-bit) | Required |
| **Python Runtime** | Version 3.10 (strict requirement) | [python.org](https://www.python.org/downloads/) |
| **AI Infrastructure** | Ollama (latest stable release) | [ollama.com](https://ollama.com/) |
| **Messaging Platform** | Telegram bot token | [@BotFather](https://t.me/BotFather) |
| **Storage** | 6 GB available (AI model) | Minimum |
| **Memory** | 8 GB RAM (16 GB recommended) | Minimum |

**Installation Note:** During Python installation, enable the "Add Python to PATH" option to ensure proper system integration.

---

## Installation

### Automated Deployment (Recommended)

The automated installer handles complete system configuration:

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/zyron-assistant.git
cd zyron-assistant

# Execute automated setup
setup.bat
```

**Automated Setup Process:**
- Python installation verification
- Virtual environment creation and activation
- Dependency installation from requirements.txt
- AI model download and configuration (qwen2.5-coder:7b)
- Windows startup integration
- Stealth mode configuration

### Manual Installation

For users requiring granular control over the installation process:

<details>
<summary><strong>Expand Manual Installation Guide</strong></summary>

#### Step 1: Ollama & AI Model Configuration

```bash
# Install Ollama from https://ollama.com/
# After installation, download the AI model:
ollama pull qwen2.5-coder:7b

# Verify installation:
ollama run qwen2.5-coder:7b
# Exit test session with: /bye
```

#### Step 2: Environment Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/zyron-assistant.git
cd zyron-assistant

# Create isolated Python environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install project dependencies
pip install -r requirements.txt
```

#### Step 3: Environment Configuration

Create `.env` file in project root:

```env
# Telegram Bot Configuration
TELEGRAM_TOKEN=your_bot_token_here

# AI Model Selection
MODEL_NAME=qwen2.5-coder:7b

# Optional: Advanced Configuration
LOG_LEVEL=INFO
MAX_TOKENS=2048
```

#### Step 4: Telegram Bot Provisioning

1. Open Telegram and initiate conversation with @BotFather
2. Send command: `/newbot`
3. Follow the interactive setup process
4. Copy the provided token to `.env` file

#### Step 5: Launch Assistant

```bash
# Standard mode (visible console)
python main.py

# Stealth mode (hidden background process)
run_silent.vbs
```

</details>

### Browser Activity Monitoring Setup

To enable comprehensive browser activity tracking with full URL visibility:

1. Navigate to your browser's extension management interface:
   - Chrome: `chrome://extensions`
   - Brave: `brave://extensions`
   - Edge: `edge://extensions`

2. Enable Developer Mode (toggle switch in top-right corner)

3. Click "Load unpacked" and select the `browser_extension` directory from your installation

4. Verify the extension is active (green indicator)

The assistant can now track active browser tabs and their URLs in real-time.

---

## Configuration

### Telegram Bot Integration

**Bot Creation Process:**

1. Initiate conversation with @BotFather on Telegram
2. Execute command: `/newbot`
3. Provide bot name: `My Zyron Assistant`
4. Provide bot username: `myzyron_bot` (must end with `_bot`)

**Token Configuration:**

1. BotFather will provide an authentication token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
2. Open `.env` file in project root
3. Update `TELEGRAM_TOKEN` variable with your token
4. Save file and restart the assistant

### Voice Control Configuration

Configure voice activation settings:

```python
# In config.py or .env:
ENABLE_VOICE=True
WAKE_WORD="hey zyron"  # Customize activation phrase
```

### Auto-Start Configuration

The installer automatically configures Windows startup integration. To manage:

**Enable Auto-Start:**
```bash
setup.bat  # Re-execute installer
```

**Disable Auto-Start:**
```bash
# Remove startup shortcut from:
# %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\ZyronAgent.lnk
```

---

## Usage

### Launch Methods

After installation, three launch options are available:

```bash
# Method 1: Automatic startup (post-reboot)
# Launches automatically in stealth mode after system boot

# Method 2: Manual stealth launch
run_silent.vbs

# Method 3: Console mode (debugging)
venv\Scripts\activate
start_pikachu.bat
```

### Command Reference

**System Control Operations**
```plaintext
/open [app]      → Launch specified application
/shutdown        → Initiate system shutdown
/sleep           → Enter sleep mode
/restart         → System reboot
/lock            → Lock workstation
```

**Information Retrieval**
```plaintext
/status          → System health metrics (CPU, RAM, Battery)
/battery         → Battery status and charge level
/screenshot      → Screen capture
/webcam          → Webcam image capture
/activities      → Running applications and browser tabs
/location        → IP-based geolocation data
```

**File Management**
```plaintext
/files           → Directory listing (current location)
/download [path] → Transfer file to Telegram
/upload          → Receive file from Telegram
```

**Audio Recording**
```plaintext
/record          → 10-second dual-source audio capture
                   (system audio + microphone input)
```

**AI Assistant Interface**
```plaintext
/ask [question]  → Natural language query processing
/help            → Command reference display
/about           → System information summary
```

### Voice Command Interface

Activate using wake word, then issue command:

```plaintext
Hey Zyron, open Chrome
Hey Zyron, what's my battery level?
Hey Zyron, take a screenshot
Hey Zyron, show me current activities
Hey Zyron, record audio
```

---

## Advanced Configuration

### Custom Command Development

Extend functionality by editing `commands.py`:

```python
@bot.command("custom")
async def custom_command(ctx):
    # Implementation logic
    await ctx.send("Custom command executed successfully")
```

### AI Model Selection

Modify AI model in `.env` configuration:

```env
# Lightweight model (3B parameters)
MODEL_NAME=qwen2.5-coder:3b

# Enhanced model (14B parameters)
MODEL_NAME=qwen2.5-coder:14b
```

### Logging Configuration

Adjust logging verbosity in `.env`:

```env
LOG_LEVEL=DEBUG    # Comprehensive debugging output
LOG_LEVEL=INFO     # Standard operational logging (default)
LOG_LEVEL=WARNING  # Warning and error events only
LOG_LEVEL=ERROR    # Critical errors only
```

---

## Troubleshooting

### Common Issues & Resolutions

<details>
<summary><strong>Python Runtime Not Found</strong></summary>

**Resolution:**
1. Reinstall Python from [python.org](https://python.org)
2. Ensure "Add Python to PATH" is checked during installation
3. Restart terminal/command prompt
4. Verify installation: `python --version`

</details>

<details>
<summary><strong>Ollama Not Detected</strong></summary>

**Resolution:**
1. Install Ollama from [ollama.com](https://ollama.com)
2. Verify installation: `ollama --version`
3. Download required model: `ollama pull qwen2.5-coder:7b`
4. Restart the assistant

</details>

<details>
<summary><strong>Telegram Bot Unresponsive</strong></summary>

**Resolution:**
1. Verify correct token in `.env` file
2. Confirm process is running (check Task Manager for `python.exe`)
3. Test bot connectivity via Telegram message
4. Review logs: `logs/assistant.log`

</details>

<details>
<summary><strong>Voice Commands Not Processing</strong></summary>

**Resolution:**
1. Verify microphone permissions in Windows Settings
2. Confirm `ENABLE_VOICE=True` in `.env`
3. Test wake word detection in console mode
4. Ensure microphone is set as default input device

</details>

<details>
<summary><strong>Activity Monitor Showing N/A URLs</strong></summary>

**Resolution:**
1. Verify browser extension installation (see Setup section)
2. Confirm browser compatibility (Chrome, Brave, Edge)
3. Reload extension in browser's extension management interface
4. Check extension permissions are granted

</details>

---

## Project Structure

```plaintext
zyron-assistant/
├── .gitignore                 # Version control exclusions
├── README.md                  # Project documentation
├── brain.py                   # AI inference engine (Ollama integration)
├── listener.py                # Voice wake word detection system
├── main.py                    # Application entry point
├── memory.py                  # Conversation context management
├── muscles.py                 # System automation controller
├── requirements.txt           # Python dependency specifications
├── run_silent.vbs            # Background process launcher
├── setup.bat                  # Automated installation script
├── start_zyron.bat           # Quick launch utility
├── tele_agent.py             # Telegram bot handler
├── test_mic.py               # Microphone diagnostic tool
├── activity_monitor.py       # Application and browser tracking
├── browser_extension/         # Browser activity monitoring extension
│   ├── manifest.json         # Extension configuration
│   ├── background.js         # Background service worker
│   ├── popup.html           # Extension UI
│   └── popup.js             # Extension logic
├── .env                      # Environment configuration (user-created)
└── venv/                     # Python virtual environment
```

### Component Descriptions

| Component | Responsibility |
|-----------|----------------|
| `brain.py` | AI inference via Ollama (qwen2.5-coder:7b model) |
| `listener.py` | Voice activation and wake word processing |
| `tele_agent.py` | Telegram API integration and command routing |
| `muscles.py` | System control operations (applications, files, media) |
| `memory.py` | Conversation history and context persistence |
| `activity_monitor.py` | Application and browser session tracking |
| `browser_extension/` | Browser tab monitoring extension source |
| `setup.bat` | Automated installer with dependency management |
| `run_silent.vbs` | Background launcher for stealth operation |
| `test_mic.py` | Microphone functionality verification |

---

## Release Notes

### Version 1.2 - Current Release

**Activity Monitoring System**
- Real-time tracking of active browser tabs with full URL visibility
- Desktop application detection and monitoring
- System resource utilization tracking
- Command: `/activities` or voice: "Hey Zyron, show activities"

**Audio Recording Capability**
- Dual-source audio capture (system + microphone)
- 10-second recording duration with automatic processing
- Telegram delivery integration

**Geolocation Services**
- IP-based location tracking implementation
- City, region, and country identification
- Command: `/location` or voice: "Hey Zyron, where am I?"
- Note: Accuracy subject to IP geolocation database precision

**Auto-Start Integration**
- Windows startup configuration during installation
- Default stealth mode operation
- Minimal boot time impact

**Storage Analysis**
- Comprehensive drive scanning for all partitions (C:, D:, etc.)
- Visual usage status indicators (🟢/🟡/🔴)
- Detailed breakdown of used vs. free space (GB) and percentage
- Command: /storage or voice: "Hey Zyron, check storage"

**Recycle Bin Management**
- Instant permanent deletion of all Recycle Bin contents across all drives
- Rapid execution time (typically clears in seconds)
- Command: /clear_bin or voice: "Hey Zyron, clear the bin"

---

## Contributing

Contributions are welcome. Follow these guidelines:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/NewCapability`
3. Commit changes: `git commit -m 'Add NewCapability'`
4. Push to branch: `git push origin feature/NewCapability`
5. Submit Pull Request

### Development Environment Setup

```bash
# Clone forked repository
git clone https://github.com/YOUR_USERNAME/zyron-assistant.git
cd zyron-assistant

# Create development branch
git checkout -b dev

# Install development dependencies
pip install -r requirements-dev.txt

# Execute test suite
pytest tests/
```

---

## Frequently Asked Questions

**Q: Is user data transmitted to external servers?**  
A: No. All processing occurs locally on your machine. Ollama handles AI inference entirely offline.

**Q: Is macOS or Linux support available?**  
A: Currently Windows-only due to system automation dependencies. Cross-platform support is planned for future releases.

**Q: What are the memory requirements during operation?**  
A: Approximately 2-4 GB while idle, 6-8 GB during active AI processing.

**Q: Can alternative AI models be used?**  
A: Yes. Any Ollama-compatible model can be configured via the `MODEL_NAME` variable in `.env`.

**Q: Is Telegram integration mandatory?**  
A: Telegram is required for remote control functionality. Voice-only operation mode is planned for future releases.

**Q: How can I contribute to the project?**  
A: See the Contributing section for detailed guidelines.

**Q: Does auto-start impact system boot performance?**  
A: No. The assistant launches as a background process after Windows initialization, using minimal system resources.

**Q: How do I disable the activity monitoring feature?**  
A: Uninstall the browser extension and remove the `activity_monitor.py` file from the project directory.

---

## License

This project is licensed under the MIT License. See the LICENSE file for complete terms.

```plaintext
MIT License - Free to use, modify, and distribute
Copyright © 2025 Zyron Desktop Assistant
```

---

## Acknowledgments

This project builds upon the following open-source technologies:

- [Ollama](https://ollama.com/) - Local AI infrastructure and model serving
- [Qwen Team](https://qwenlm.github.io/) - Qwen 2.5 Coder language model
- [python-telegram-bot](https://python-telegram-bot.org/) - Telegram Bot API wrapper
- Community contributors and testers

---

## Support & Documentation

**Documentation Resources**
- Comprehensive Wiki: [Documentation](https://github.com/Surajkumar5050/pikachu-assistant/tree/main/docs)
- Bug Reports: [Issue Tracker](https://github.com/Surajkumar5050/pikachu-assistant/issues)
- Community Discussion: [GitHub Discussions](https://github.com/Surajkumar5050/pikachu-assistant/issues)

---

<div align="center">

**If this project adds value to your workflow, please consider starring the repository.**

*Developed with precision and attention to detail*

[Return to Top](#zyron-desktop-assistant)

</div>