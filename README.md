# Forwardbot
# owner:- https://t.me/Adityaji5
# Telegram Auto Forward Bot

A premium asynchronous Python-based bot utilizing Pyrogram framework to securely sync multiclient operations.

## Deployment Installation Guide

### Prerequisites
- Python 3.11+
- MongoDB instance URI string
- Telegram API ID & Hash credentials

### Setup Steps
1. Clone your project workspace directory onto your target Linux environment / Termux shell.
2. Initialize environment keys variables via an `.env` file configuration file container wrapper:

```env
API_ID=1234567
API_HASH=abcdef1234567890
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx
MONGO_URI=mongodb+srv://...
DB_NAME=forwarder_bot
ADMIN_IDS=987654321
ENCRYPTION_KEY=YourSuperSecretUnsharedTokenKey32B!
SOURCE_CHAT_ID=-1000123456789
