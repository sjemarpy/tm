import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8866016258:AAGIvXLKvH2qPHzhEPnD863oj_ZGOPO20tc")

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Bot Configuration
DEFAULT_MODEL = "openai/gpt-3.5-turbo"
MAX_CONVERSATION_HISTORY = 20
MAX_MESSAGE_LENGTH = 4096
REQUEST_TIMEOUT = 30

# Admin Configuration (replace with your Telegram user ID)
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]

# Available Models
AVAILABLE_MODELS = {
    "gpt-3.5": "openai/gpt-3.5-turbo",
    "gpt-4": "openai/gpt-4",
    "claude": "anthropic/claude-3-sonnet",
    "llama": "meta-llama/llama-3-70b-instruct",
    "mistral": "mistralai/mistral-7b-instruct"
}

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "logs/bot.log"
