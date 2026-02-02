import logging
import asyncio
import os
from dotenv import load_dotenv
from telegram import Update, constants, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from brain import process_command
from muscles import execute_command, capture_webcam
import memory
import activity_monitor  # <--- NEW IMPORT: Needed to format the output text

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    print("❌ Error: TELEGRAM_TOKEN not found in .env file.")
    exit()

ALLOWED_USERS = [] 

CAMERA_ACTIVE = False

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_main_keyboard():
    # Added "Activities" button to the layout
    keyboard = [
        [KeyboardButton("/screenshot"), KeyboardButton("/sleep")],
        [KeyboardButton("/activities"), KeyboardButton("/camera_on")], 
        [KeyboardButton("/batterypercentage"), KeyboardButton("/systemhealth")],
        [KeyboardButton("/location"), KeyboardButton("/recordaudio")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def safe_send_action(bot, chat_id, action):
    """Safely send chat action (typing/uploading) without crashing on timeout"""
    try:
        await bot.send_chat_action(chat_id=chat_id, action=action)
    except Exception as e:
        print(f"⚠️ Network Warning: Could not send chat action: {e}")

async def camera_monitor_loop(bot, chat_id):
    global CAMERA_ACTIVE
    try:
        await bot.send_message(chat_id, "🔴 Live Feed Started...")
    except: pass
    
    while CAMERA_ACTIVE:
        photo_path = capture_webcam()
        if photo_path and os.path.exists(photo_path):
            try:
                await bot.send_photo(chat_id, photo=open(photo_path, 'rb'))
            except Exception:
                pass # Ignore network errors during stream
        await asyncio.sleep(3) 
    
    try:
        await bot.send_message(chat_id, "⏹️ Camera Feed Stopped.")
    except: pass


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"⚡ **Pikachu Online!**\nHello {user}. Use the buttons below.",
        reply_markup=get_main_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CAMERA_ACTIVE
    user_text = update.message.text
    sender = update.message.from_user.username
    chat_id = update.effective_chat.id
    lower_text = user_text.lower()
    
    print(f"\n📩 Message from @{sender}: {user_text}")

    # 1. Safe "Typing" Indicator (Won't crash if internet lags)
    await safe_send_action(context.bot, chat_id, constants.ChatAction.TYPING)

    # Pre-process common commands
    command_json = None
    
    if "/battery" in lower_text or "battery" in lower_text:
        command_json = {"action": "check_battery"}
    elif "/systemhealth" in lower_text or "system health" in lower_text:
        command_json = {"action": "check_health"}
    elif "/screenshot" in lower_text or "screenshot" in lower_text:
        command_json = {"action": "take_screenshot"}
    elif "/sleep" in lower_text:
        command_json = {"action": "system_sleep"}
    elif "/camera_on" in lower_text:
        command_json = {"action": "camera_stream", "value": "on"}
    elif "/camera_off" in lower_text:
        command_json = {"action": "camera_stream", "value": "off"}
    elif "/recordaudio" in lower_text or "record audio" in lower_text:
        command_json = {"action": "record_audio", "duration": 10}
    elif "/location" in lower_text or any(x in lower_text for x in ["my location", "where am i", "laptop location", "where is my laptop", "find location"]):
        command_json = {"action": "get_location"}
    # Added explicit check for activities command
    elif "/activities" in lower_text or "activities" in lower_text:
        command_json = {"action": "get_activities"}

    # Show processing message (with error handling)
    status_msg = None
    try:
        status_msg = await update.message.reply_text("⚡ Thinking...", reply_markup=get_main_keyboard())
    except Exception:
        pass # If we can't send "Thinking", just continue

    if not command_json:
        loop = asyncio.get_running_loop()
        try:
            # Use AI to process command
            command_json = await loop.run_in_executor(None, process_command, user_text)
        except Exception as e:
            # If AI fails, send error
            if status_msg: await status_msg.delete()
            await update.message.reply_text(f"❌ Brain Error: {e}", reply_markup=get_main_keyboard())
            return


    if command_json:
        action = command_json.get('action')
        
        # --- NEW: ACTIVITIES HANDLER ---
        if action == "get_activities":
            if status_msg: await status_msg.delete()
            # 1. Get raw data from muscles (which calls activity_monitor)
            raw_data = execute_command(command_json)
            
            if raw_data:
                # 2. Format the data using the helper function in activity_monitor
                formatted_message = activity_monitor.format_activities_text(raw_data)
                # 3. Send the nicely formatted text
                try:
                    await update.message.reply_text(formatted_message, parse_mode='Markdown', reply_markup=get_main_keyboard())
                except Exception as e:
                    await update.message.reply_text(f"❌ Error displaying activities: {e}", reply_markup=get_main_keyboard())
            else:
                await update.message.reply_text("❌ Could not fetch activities.", reply_markup=get_main_keyboard())

        # --- LOCATION TRACKING ---
        elif action == "get_location":
            if status_msg: await status_msg.delete()
            loader = await update.message.reply_text("📍 Checking multiple location sources...", reply_markup=get_main_keyboard())
            
            # Get location data
            location_data = execute_command(command_json)
            
            if location_data:
                # Format location message
                location_text = f"""📍 **Laptop Location**

🌍 **Location:** {location_data['city']}, {location_data['region']}
🏳️ **Country:** {location_data['country']} ({location_data['country_code']})
📮 **Postal Code:** {location_data['postal']}
🌐 **IP Address:** {location_data['ip']}
📡 **ISP:** {location_data['org']}
🕐 **Timezone:** {location_data['timezone']}

📌 **Coordinates:**
Latitude: {location_data['latitude']}
Longitude: {location_data['longitude']}

🔍 **Data Source:** {location_data['source']}

🗺️ [**Open in Google Maps**]({location_data['maps_url']})
"""
                
                # Add comparison if multiple sources were checked
                if location_data.get('comparison'):
                    location_text += f"\n\n⚠️ **Location Comparison:**\n{location_data['comparison']}\n\n_Note: IP-based location may be 50-200km from your actual position. This shows your ISP's server location._"
                
                await loader.delete()
                
                # Send location as text
                await update.message.reply_text(
                    location_text,
                    parse_mode='Markdown',
                    disable_web_page_preview=False,
                    reply_markup=get_main_keyboard()
                )
                
                # Send location on map (Telegram native location)
                try:
                    await update.message.reply_location(
                        latitude=location_data['latitude'],
                        longitude=location_data['longitude'],
                        reply_markup=get_main_keyboard()
                    )
                except Exception as e:
                    print(f"Could not send map location: {e}")
                    
            else:
                await loader.edit_text("❌ Failed to get location. Check internet connection.", reply_markup=get_main_keyboard())
        
        # --- BATTERY CHECK ---
        elif action == "check_battery":
            status = execute_command(command_json)
            if status_msg: await status_msg.delete()
            await update.message.reply_text(f"🔋 {status}", reply_markup=get_main_keyboard())
            
        elif action == "check_health":
            report = execute_command(command_json)
            if status_msg: await status_msg.delete()
            await update.message.reply_text(report, reply_markup=get_main_keyboard())
            
        elif action == "take_screenshot":
            # Screenshot
            if status_msg: await status_msg.delete()
            loader = await update.message.reply_text("📸 Capture...", reply_markup=get_main_keyboard())
            path = execute_command(command_json)
            if path:
                try:
                    await update.message.reply_photo(photo=open(path, 'rb'))
                    await loader.delete()
                except Exception as e:
                    await loader.edit_text(f"❌ Upload Failed: {e}")
            else:
                await loader.edit_text("❌ Screenshot failed.")
                
        elif action == "system_sleep":
            if status_msg: await status_msg.delete()
            await update.message.reply_text("💤 Goodnight.", reply_markup=get_main_keyboard())
            execute_command(command_json)

        elif action == "camera_stream":
            val = command_json.get("value")
            if status_msg: await status_msg.delete()
            if val == "on":
                if not CAMERA_ACTIVE:
                    CAMERA_ACTIVE = True
                    asyncio.create_task(camera_monitor_loop(context.bot, chat_id))
            else:
                CAMERA_ACTIVE = False
                await update.message.reply_text("🛑 Stopping Camera...", reply_markup=get_main_keyboard())

        elif action == "record_audio":
            if status_msg: await status_msg.delete()
            duration = command_json.get("duration", 10)
            loader = await update.message.reply_text(f"🎤 Recording audio for {duration} seconds...", reply_markup=get_main_keyboard())
            
            # Execute audio recording in executor to avoid blocking
            loop = asyncio.get_running_loop()
            audio_path = await loop.run_in_executor(None, execute_command, command_json)
            
            if audio_path and os.path.exists(audio_path):
                try:
                    await loader.delete()
                except:
                    pass  # Ignore if message already deleted
                
                # Send the audio file
                try:
                    await update.message.reply_audio(audio=open(audio_path, 'rb'), caption="🎵 Recorded Audio (10 seconds)")
                except Exception as e:
                     await update.message.reply_text(f"❌ Upload Failed: {e}")
            else:
                try:
                    await loader.edit_text("❌ Audio recording failed.")
                except:
                    await update.message.reply_text("❌ Audio recording failed.", reply_markup=get_main_keyboard())

        elif action == "general_chat":
            response = command_json.get('response', "...")
            # AI chat response
            if status_msg: await status_msg.delete()
            await update.message.reply_text(f"💬 {response}", reply_markup=get_main_keyboard())
            
        # --- File / App Handling ---
        elif action == "list_files":
            if status_msg: await status_msg.delete()
            raw_path = command_json.get('path')
            if "desktop" in raw_path.lower(): raw_path = os.path.join(os.path.expanduser("~"), "Desktop")
            elif "downloads" in raw_path.lower(): raw_path = os.path.join(os.path.expanduser("~"), "Downloads")
            
            if os.path.exists(raw_path):
                try:
                    files = os.listdir(raw_path)[:20]
                    text = "\n".join([f"📹 {f}" for f in files])
                    await update.message.reply_text(f"📂 **Files:**\n{text}", reply_markup=get_main_keyboard())
                except: 
                    await update.message.reply_text("❌ Failed to read folder.", reply_markup=get_main_keyboard())
            else:
                await update.message.reply_text("❌ Folder not found.", reply_markup=get_main_keyboard())

        elif action == "send_file":
             if status_msg: await status_msg.delete()
             raw_path = command_json.get('path')
             if os.path.exists(raw_path):
                 try:
                     await update.message.reply_text("📤 Uploading...", reply_markup=get_main_keyboard())
                     # SAFE UPLOAD: Tries to upload, catches errors if file is too big or net is slow
                     await update.message.reply_document(open(raw_path, 'rb'))
                 except Exception as e:
                     print(f"Upload Error: {e}")
                     await update.message.reply_text("❌ Error: File upload timed out or failed.", reply_markup=get_main_keyboard())
             else:
                 await update.message.reply_text("❌ File not found.", reply_markup=get_main_keyboard())

        else:
            # Generic action execution
            try:
                execute_command(command_json)
                if status_msg: await status_msg.delete()
                await update.message.reply_text(f"✅ Action Complete: {action}", reply_markup=get_main_keyboard())
            except Exception as e:
                if status_msg: await status_msg.delete()
                await update.message.reply_text(f"❌ Error: {e}", reply_markup=get_main_keyboard())

if __name__ == "__main__":
    print("🚀 TELEGRAM BOT STARTED...")
    try:
        # Increase connection timeout to handle slow uploads better
        application = ApplicationBuilder().token(TOKEN).read_timeout(60).write_timeout(60).build()
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(MessageHandler(filters.TEXT | filters.COMMAND, handle_message))
        application.run_polling()
    except Exception as e:
        print(f"❌ Critical Error: {e}")