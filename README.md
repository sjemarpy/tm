# 🤖 Telegram AI Bot

একটি AI-powered Telegram bot যা OpenRouter API ব্যবহার করে।

## ✨ Features

- 🧠 Multiple AI models support (GPT-3.5, GPT-4, Claude, Llama, Mistral)
- 💬 Conversation history management
- 🌐 Multi-language support (Bengali, English, etc.)
- 📊 User statistics
- 🔐 Admin controls
- 📝 Error handling and logging
- ⚡ Fast and responsive

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/telegram-ai-bot.git
cd telegram-ai-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` file and add your credentials:
- `TELEGRAM_TOKEN`: Your Telegram bot token from @BotFather
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `ADMIN_IDS`: Your Telegram user ID (optional)

### 4. Run the bot

```bash
python bot.py
```

## 📱 Usage

### Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/model` - Change AI model
- `/clear` - Clear conversation history
- `/stats` - Show your statistics
- `/admin` - Admin commands (admin only)

### Basic Usage

Just send any message to the bot, and it will respond using AI!

## 🛠️ Configuration

### Available Models

- `gpt-3.5` - OpenAI GPT-3.5 Turbo
- `gpt-4` - OpenAI GPT-4
- `claude` - Anthropic Claude 3 Sonnet
- `llama` - Meta Llama 3 70B
- `mistral` - Mistral AI 7B

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_TOKEN` | Telegram bot token | Yes |
| `OPENROUTER_API_KEY` | OpenRouter API key | Yes |
| `ADMIN_IDS` | Admin user IDs | No |
| `LOG_LEVEL` | Logging level | No |

## 🌐 Deployment

### Deploy to Heroku

1. Create a Heroku app
2. Set environment variables in Heroku dashboard
3. Push code to Heroku:

```bash
heroku git:remote -a your-app-name
git push heroku main
```

### Deploy to Railway

1. Create a new project on Railway
2. Connect your GitHub repository
3. Add environment variables
4. Deploy!

### Deploy to VPS/Server

```bash
# Install Python 3.8+
sudo apt update
sudo apt install python3 python3-pip

# Clone and setup
git clone https://github.com/yourusername/telegram-ai-bot.git
cd telegram-ai-bot
pip3 install -r requirements.txt

# Run with screen or tmux
screen -S telegram-bot
python3 bot.py
# Press Ctrl+A, then D to detach
```

## 🔒 Security

- Never commit `.env` file to GitHub
- Keep your API keys secure
- Use environment variables for sensitive data
- Regularly update dependencies

## 📝 Logging

Logs are stored in `logs/bot.log`. You can change the log level in `.env` file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created with ❤️ for the community.

## 🆘 Support

If you encounter any issues, please open an issue on GitHub.

---

**Note:** This bot uses OpenRouter API which may have usage limits and costs. Please check OpenRouter's pricing before heavy usage.
