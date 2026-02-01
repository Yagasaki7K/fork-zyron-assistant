# ⚙️ Configuration Guide

This document explains how to configure the **"Senses"** (Telegram & Voice) and the **"Brain"** (AI Model) of your Pikachu Assistant.

---

## 🤖 1. Setting Up the Telegram Bot

To control your PC remotely, you need a **free Telegram Bot Token**.

### **Step-by-Step:**

1. **Open Telegram** and search for [@BotFather](https://t.me/BotFather)

2. **Click Start** (or type `/start`)

3. **Send the command**: `/newbot`

4. **Name your bot**: 
   - Enter a display name (e.g., `My Desktop Agent`)
   - This is what users will see in their chat list

5. **Choose a username**: 
   - Must end in `bot` (e.g., `JohnPC_Controller_Bot`)
   - Must be unique across all of Telegram
   - Examples: `MyPC_bot`, `HomeAssistant_bot`, `PikachuPC_bot`

6. **Copy the Token**: 
   - BotFather will give you a long string like:
     ```
     7182934:AAFWD-1923-Oldfw234-Wsdff
     ```
   - ⚠️ **Keep this secret!** Anyone with this token can control your bot.

7. **Paste it**: 
   - Open your `.env` file in the project root
   - Paste it next to `TELEGRAM_TOKEN=`

### **Example BotFather Conversation:**

```
You: /newbot
BotFather: Alright, a new bot. How are we going to call it?

You: My Desktop Agent
BotFather: Good. Now let's choose a username for your bot.

You: JohnPC_Controller_Bot
BotFather: Done! Congratulations on your new bot.
           Token: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

---

## 📝 2. Environment Variables (.env)

The `.env` file in the root directory controls the core settings. If it doesn't exist, create it.

### **Required Variables**

| Variable | Example Value | Description |
|----------|---------------|-------------|
| `TELEGRAM_TOKEN` | `12345:ABC-DEF...` | **Required**. The token you got from BotFather. |
| `MODEL_NAME` | `qwen2.5-coder:7b` | **Required**. The Ollama model to use. |

### **Optional Variables**

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Set to `DEBUG` for more verbose output. Options: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama API endpoint (change if running on a different machine) |
| `WAKE_WORDS` | `pikachu,hey you` | Comma-separated list of wake words (future feature) |
| `VOICE_RATE` | `150` | Speech speed (words per minute). Range: 100-200 |
| `VOICE_VOLUME` | `1.0` | TTS volume. Range: 0.0-1.0 |

### **Example `.env` File**

```ini
# Telegram Bot Configuration
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# AI Model Settings
MODEL_NAME=qwen2.5-coder:7b
OLLAMA_URL=http://localhost:11434

# Optional: Logging
LOG_LEVEL=INFO

# Optional: Voice Settings
VOICE_RATE=150
VOICE_VOLUME=0.8
```

### **Important Notes:**

- ✅ **No quotes needed** around values
- ✅ **No spaces** around the `=` sign
- ✅ **Comments** can be added with `#`
- ⚠️ **Never commit `.env` to Git** - it's already in `.gitignore`

---

## 🧠 3. Changing the AI Model

Pikachu uses **Qwen 2.5 Coder (7B)** by default because it excels at following JSON instructions. However, you can swap it for any model Ollama supports.

### **To Use a Different Model:**

**1. Download the model via terminal:**

```bash
ollama pull llama3
```

**2. Update Config:**

Open `.env` and change:

```ini
MODEL_NAME=llama3
```

**3. Restart:**

Close and re-run the assistant.

---

### **Recommended Models**

| Model | Size | Speed | JSON Accuracy | Best For |
|-------|------|-------|---------------|----------|
| **`qwen2.5-coder:7b`** ⭐ | 4.7GB | Fast | Excellent | **Default choice** - Best balance |
| `llama3:8b` | 4.7GB | Fast | Good | General conversation |
| `mistral:7b` | 4.1GB | Very Fast | Good | Quick responses |
| `codellama:7b` | 3.8GB | Fast | Very Good | Code-heavy tasks |
| `qwen2.5-coder:3b` | 2.0GB | Very Fast | Fair | Low-end PCs |
| `llama3.2:3b` | 2.0GB | Very Fast | Fair | Budget option |

### **Advanced: Model Performance Tuning**

If the model is too slow or inaccurate, you can adjust Ollama parameters by creating a `Modelfile`:

```dockerfile
FROM qwen2.5-coder:7b

# Increase speed at the cost of quality
PARAMETER temperature 0.7

# Control randomness (lower = more deterministic)
PARAMETER top_p 0.9

# Number of tokens to predict
PARAMETER num_predict 512
```

Then create a custom model:

```bash
ollama create mymodel -f Modelfile
```

And update `.env`:

```ini
MODEL_NAME=mymodel
```

---

### **Switching Between Models on the Fly**

You can temporarily override the model without editing `.env`:

```bash
# For voice mode
MODEL_NAME=llama3 python main.py

# For Telegram mode
MODEL_NAME=mistral python tele_agent.py
```

---

## 🗣️ 4. Customizing Voice & Wake Words

Currently, wake words are defined in the code for performance reasons.

### **To Change the Wake Word** (Default: "Pikachu")

**1. Open `listener.py`** in a text editor (VS Code / Notepad)

**2. Locate the `WAKE_WORDS` list** near the top:

```python
WAKE_WORDS = ["pikachu", "pika", "peek a", "pick a", "hey you"]
```

**3. Add your own words** (lowercase only):

```python
WAKE_WORDS = ["jarvis", "computer", "hey system"]
```

**4. Save and restart** the assistant

---

### **Wake Word Best Practices**

✅ **DO:**
- Use phonetically distinct words ("jarvis", "alexa", "computer")
- Include phonetic variations ("peek a", "pika" for "Pikachu")
- Keep them 2+ syllables for better detection

❌ **DON'T:**
- Use common words ("hello", "okay", "yes")
- Use names of people in your household
- Use words that appear in normal conversation

---

### **Advanced: Adjusting Voice Recognition Sensitivity**

In `listener.py`, you can tune the speech recognition parameters:

```python
# Adjust these values for better detection
recognizer = sr.Recognizer()
recognizer.energy_threshold = 4000  # Lower = more sensitive (default: 4000)
recognizer.dynamic_energy_threshold = True  # Auto-adjust to ambient noise
recognizer.pause_threshold = 0.8  # Seconds of silence before considering input complete
```

**Troubleshooting:**
- **Too many false positives?** → Increase `energy_threshold` to 5000+
- **Not detecting your voice?** → Decrease `energy_threshold` to 2000-3000
- **Cuts you off mid-sentence?** → Increase `pause_threshold` to 1.0-1.5

---

### **Changing TTS Voice**

The assistant uses `pyttsx3` for text-to-speech. You can customize the voice:

**In `listener.py` or wherever TTS is initialized:**

```python
import pyttsx3

engine = pyttsx3.init()

# List available voices
voices = engine.getProperty('voices')
for voice in voices:
    print(voice.id, voice.name)

# Set a specific voice (use ID from above)
engine.setProperty('voice', voices[1].id)  # Usually female voice on Windows

# Adjust speech rate (words per minute)
engine.setProperty('rate', 150)  # Default: 200

# Adjust volume (0.0 to 1.0)
engine.setProperty('volume', 0.8)
```

---

## 📸 5. Camera & Security Settings

### **Telegram Camera Feed**

The Telegram bot can stream your webcam.

⚠️ **Privacy Warning**: Anyone with your Bot Token can access this. **Do not share your `.env` file.**

---

### **Restricting Access to Specific Users**

To restrict access to only you:

**1. Find your Telegram username:**
- Open Telegram
- Go to Settings
- Your username is shown as `@YourUsername`

**2. Open `tele_agent.py`** and locate:

```python
# Near the top of the file
ALLOWED_USERS = []  # Empty = anyone can use the bot
```

**3. Add your username** (without the `@`):

```python
ALLOWED_USERS = ["YourUsername"]  # Replace with your actual username
```

**4. Uncomment the user check logic:**

Find this section (usually in the message handler):

```python
# if update.effective_user.username not in ALLOWED_USERS:
#     await update.message.reply_text("⛔ Unauthorized user.")
#     return
```

**Uncomment it:**

```python
if update.effective_user.username not in ALLOWED_USERS:
    await update.message.reply_text("⛔ Unauthorized user.")
    return
```

**5. Restart the bot**

---

### **Multi-User Access**

To allow multiple trusted users:

```python
ALLOWED_USERS = ["alice", "bob", "charlie"]
```

---

### **Disabling Camera Access Entirely**

If you want to remove camera functionality:

**Option 1: Comment out camera commands in `tele_agent.py`:**

```python
# Find and comment out camera-related handlers
# application.add_handler(CommandHandler("camera", camera_command))
```

**Option 2: Add a hard block in `muscles.py`:**

```python
def start_camera():
    raise PermissionError("Camera access disabled by user")
```

---

### **Advanced: Logging Bot Activity**

To track who's using your bot and what commands they send:

**Add this to `tele_agent.py`:**

```python
import logging
from datetime import datetime

# Enable logging
logging.basicConfig(
    filename='bot_activity.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# In your message handler
async def handle_message(update, context):
    user = update.effective_user.username
    message = update.message.text
    logging.info(f"User: {user} | Message: {message}")
    # ... rest of your code
```

This creates a `bot_activity.log` file with all interactions.

---

## 🔒 6. Security Best Practices

### **Token Security**

✅ **DO:**
- Keep `.env` in `.gitignore`
- Never share your `.env` file
- Regenerate token if exposed (via BotFather: `/revoke`)
- Use environment variables in production

❌ **DON'T:**
- Commit `.env` to GitHub
- Share screenshots containing tokens
- Use the same token for multiple bots

---

### **System Access Control**

The bot has broad permissions by default. Consider:

**1. Sandboxing file operations:**

```python
# In muscles.py
SAFE_DIRECTORIES = [
    "C:/Users/YourName/Documents",
    "C:/Users/YourName/Downloads"
]

def list_files(directory):
    if not any(directory.startswith(safe) for safe in SAFE_DIRECTORIES):
        raise PermissionError("Access to this directory is restricted")
    # ... rest of function
```

**2. Disabling dangerous commands:**

```python
# In brain.py
DISABLED_ACTIONS = ["shutdown", "delete_file", "close_app"]

def process_command(command):
    if command["action"] in DISABLED_ACTIONS:
        return {"error": "This action is disabled for safety"}
    # ... rest of function
```

---

## 🔧 7. Advanced Configuration

### **Remote Ollama Server**

If you're running Ollama on a different machine:

```ini
OLLAMA_URL=http://192.168.1.100:11434
```

Make sure Ollama is configured to accept remote connections:

```bash
# On the Ollama server machine
OLLAMA_HOST=0.0.0.0 ollama serve
```

---

### **Custom System Prompts**

To change how the AI behaves, edit `brain.py`:

```python
BASE_SYSTEM_PROMPT = """
You are a helpful desktop assistant named Pikachu.
You MUST respond only with valid JSON.
Available actions: {actions}

Personality: Be friendly but concise.
"""
```

---

### **Webhook Mode (Advanced)**

For production deployments, use webhooks instead of polling:

**In `tele_agent.py`:**

```python
# Replace polling with webhook
application.run_webhook(
    listen="0.0.0.0",
    port=8443,
    url_path="telegram",
    webhook_url="https://yourdomain.com:8443/telegram"
)
```

Requires SSL certificate and public domain.

---

## ✅ Configuration Checklist

Before running the assistant, verify:

- [ ] `.env` file exists with valid `TELEGRAM_TOKEN`
- [ ] `MODEL_NAME` matches a downloaded Ollama model
- [ ] Wake words are customized (if desired)
- [ ] User restrictions are configured (if desired)
- [ ] Camera access is controlled (if privacy-sensitive)
- [ ] Log level is appropriate (`INFO` for normal use)

---

## 🆘 Common Configuration Issues

### Issue: "Unauthorized" error from Telegram

**Cause**: Invalid or expired token

**Fix**: Regenerate token via BotFather:
1. Message @BotFather
2. Send `/token`
3. Select your bot
4. Copy new token to `.env`

---

### Issue: Model responds but ignores JSON format

**Cause**: Model doesn't follow structured output well

**Fix**: Switch to `qwen2.5-coder:7b` which is optimized for JSON

---

### Issue: Wake word detection too slow

**Cause**: Model is processing each wake word check

**Fix**: Wake words are checked via regex, not AI. Check microphone input delay.

---

## 📚 Next Steps

- 📖 [User Guide](USER_GUIDE.md) - Learn available commands
- 🏗️ [Architecture](ARCHITECTURE.md) - Understand how it works
- 🛠️ [Development Guide](DEVELOPMENT.md) - Extend functionality

---

**Your configuration is complete! 🎉**

Start the assistant with `python main.py` (voice) or `python tele_agent.py` (Telegram).
