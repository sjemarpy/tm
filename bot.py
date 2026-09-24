import logging
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import requests
import json
from collections import defaultdict
from config import *

# Create logs directory
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, LOG_LEVEL),
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Conversation history storage
conversation_history = defaultdict(list)

# User model preferences
user_models = defaultdict(lambda: DEFAULT_MODEL)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when /start is issued."""
    user = update.effective_user
    welcome_text = f"""
🤖 *স্বাগতম {user.first_name}!*

আমি একটি AI-powered Telegram Bot। আমি OpenRouter API ব্যবহার করে আপনার প্রশ্নের উত্তর দিই।

📚 *আমি যা করতে পারি:*
• যেকোনো প্রশ্নের উত্তর দিতে পারি
• কোড লিখতে ও ব্যাখ্যা করতে পারি
• অনুবাদ করতে পারি
• লেখা ও সম্পাদনা করতে পারি
• গণিত ও সমস্যা সমাধান করতে পারি

🎯 *Commands:*
/start - Bot শুরু করুন
/help - সাহায্য বার্তা
/model - AI model পরিবর্তন করুন
/clear - Conversation history মুছে ফেলুন
/stats - আপনার পরিসংখ্যান দেখুন
/admin - Admin commands (শুধু admin এর জন্য)

💬 যেকোনো প্রশ্ন বা কাজ আমাকে পাঠান!
"""
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message."""
    help_text = """
📚 *সাহায্য বার্তা*

*Basic Commands:*
/start - Bot শুরু করুন
/help - এই সাহায্য বার্তা
/model - AI model পরিবর্তন করুন
/clear - Conversation history মুছুন
/stats - আপনার পরিসংখ্যান

*কিভাবে ব্যবহার করবেন:*
1. শুধু আমাকে message পাঠান
2. আমি AI ব্যবহার করে উত্তর দেব
3. আপনার conversation history সংরক্ষিত থাকবে

*Supported Languages:*
• বাংলা
• English
• এবং অন্যান্য ভাষা

*Tips:*
• /model command দিয়ে বিভিন্ন AI model ব্যবহার করতে পারেন
• /clear দিয়ে পুরনো conversation মুছে ফেলতে পারেন
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show model selection menu."""
    user_id = update.effective_user.id
    current_model = user_models[user_id]
    
    keyboard = []
    for name, model_id in AVAILABLE_MODELS.items():
        status = "✓" if model_id == current_model else ""
        keyboard.append([
            InlineKeyboardButton(
                f"{name.upper()} {status}",
                callback_data=f"set_model_{name}"
            )
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🤖 *বর্তমান Model:* `{current_model}`\n\n"
        "নিচের বাটন থেকে নতুন model নির্বাচন করুন:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button callbacks."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data.startswith("set_model_"):
        model_name = data.replace("set_model_", "")
        if model_name in AVAILABLE_MODELS:
            user_models[user_id] = AVAILABLE_MODELS[model_name]
            await query.edit_message_text(
                f"✅ Model পরিবর্তন হয়েছে!\n\n"
                f"নতুন Model: `{AVAILABLE_MODELS[model_name]}`",
                parse_mode='Markdown'
            )
            logger.info(f"User {user_id} changed model to {AVAILABLE_MODELS[model_name]}")

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear conversation history."""
    user_id = update.effective_user.id
    conversation_history[user_id].clear()
    
    await update.message.reply_text(
        "✅ Conversation history মুছে ফেলা হয়েছে!\n\n"
        "এখন নতুন করে শুরু করতে পারেন।"
    )
    logger.info(f"User {user_id} cleared conversation history")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics."""
    user_id = update.effective_user.id
    user = update.effective_user
    
    messages_count = len(conversation_history[user_id])
    current_model = user_models[user_id]
    
    stats_text = f"""
📊 *আপনার পরিসংখ্যান*

👤 *User:* {user.first_name}
🆔 *User ID:* `{user_id}`
💬 *Messages:* {messages_count}
🤖 *Current Model:* `{current_model}`

📅 *সংগ্রহের তারিখ:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin commands."""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ আপনি admin নন!")
        return
    
    admin_text = """
🔐 *Admin Commands*

/broadcast <message> - সব user কে message পাঠান
/users - মোট user সংখ্যা দেখুন
/clearall - সব conversation history মুছুন
"""
    
    await update.message.reply_text(admin_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages and get AI response."""
    user_message = update.message.text
    user_id = update.effective_user.id
    model = user_models[user_id]
    
    logger.info(f"User {user_id} ({update.effective_user.first_name}): {user_message}")
    
    # Send typing indicator
    await update.message.chat.send_action(action="typing")
    
    try:
        # Add user message to conversation history
        conversation_history[user_id].append({
            "role": "user",
            "content": user_message
        })
        
        # Keep conversation history within limit
        if len(conversation_history[user_id]) > MAX_CONVERSATION_HISTORY:
            conversation_history[user_id] = conversation_history[user_id][-MAX_CONVERSATION_HISTORY:]
        
        # Prepare messages for API
        messages = [
            {
                "role": "system",
                "content": "You are a helpful, friendly AI assistant. Respond in the same language as the user's message. Be concise but thorough."
            }
        ] + conversation_history[user_id]
        
        # Call OpenRouter API
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/yourusername/telegram-ai-bot",
            "X-Title": "Telegram AI Bot"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            
            # Add AI response to conversation history
            conversation_history[user_id].append({
                "role": "assistant",
                "content": ai_response
            })
            
            # Split long messages
            if len(ai_response) > MAX_MESSAGE_LENGTH:
                chunks = [ai_response[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(ai_response), MAX_MESSAGE_LENGTH)]
                for chunk in chunks:
                    await update.message.reply_text(chunk)
            else:
                await update.message.reply_text(ai_response)
                
            logger.info(f"AI response sent to user {user_id}")
            
        elif response.status_code == 429:
            await update.message.reply_text(
                "⏳ Rate limit reached! অনুগ্রহ করে কিছুক্ষণ পর আবার চেষ্টা করুন।"
            )
            logger.warning(f"Rate limit hit for user {user_id}")
            
        elif response.status_code == 401:
            await update.message.reply_text(
                "❌ API key invalid! অনুগ্রহ করে admin এর সাথে যোগাযোগ করুন।"
            )
            logger.error("Invalid API key")
            
        else:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            await update.message.reply_text(
                f"❌ Error: {error_msg}\n\nঅনুগ্রহ করে আবার চেষ্টা করুন।"
            )
            logger.error(f"API Error {response.status_code}: {error_msg}")
    
    except requests.exceptions.Timeout:
        await update.message.reply_text(
            "⏰ AI response পেতে দেরি হচ্ছে। অনুগ্রহ করে আবার চেষ্টা করুন।"
        )
        logger.error(f"Timeout for user {user_id}")
        
    except requests.exceptions.ConnectionError:
        await update.message.reply_text(
            "🌐 Internet connection সমস্যা। অনুগ্রহ করে আবার চেষ্টা করুন।"
        )
        logger.error(f"Connection error for user {user_id}")
        
    except Exception as e:
        await update.message.reply_text(
            "❌ একটি ত্রুটি ঘটেছে। অনুগ্রহ করে আবার চেষ্টা করুন।"
        )
        logger.error(f"Error for user {user_id}: {e}", exc_info=True)

def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates."""
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    """Start the bot."""
    logger.info("Starting Telegram AI Bot...")
    
    # Create application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("model", model_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Start polling
    logger.info("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
