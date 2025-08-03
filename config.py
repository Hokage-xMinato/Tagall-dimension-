import os

# Bot configuration
API_ID = int(os.getenv("API_ID", "22776206"))
API_HASH = os.getenv("API_HASH", "ada968d0b6551a6c766b864ecfeffcd5")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8046947223:AAE-vBQ6rw0pHm9JvCjSHjv1fZ5qYtR7b0A")

# Web server configuration
WEB_PORT = int(os.getenv("WEB_PORT", "5000"))
WEB_HOST = "0.0.0.0"

# For Render.com deployment, use port 10000
if os.getenv("RENDER"):
    WEB_PORT = int(os.getenv("PORT", "10000"))

# Bot settings
SESSION_NAME = "afk_bot"
EMOJIS = ["😄", "🔥", "🚀", "💥", "🐱", "🌟", "🎯", "✨"]
