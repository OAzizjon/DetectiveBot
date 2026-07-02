<h1 align="center">DetectiveBot<sub>v1.0</sub></h1>

<p align="center">
A Telegram bot that helps you look up information about your contacts — ID, full name, username, phone number, country, and mobile operator.
</p>

<p align="center">
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
<img src="https://img.shields.io/badge/aiogram_3.x-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="aiogram">
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
<img src="https://img.shields.io/badge/python--dotenv-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="dotenv">
<img src="https://img.shields.io/badge/phonenumbers-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="phonenumbers">
<img src="https://img.shields.io/badge/logging-9B59B6?style=for-the-badge&logo=fluentbit&logoColor=white" alt="logging">
<img src="https://img.shields.io/badge/lang-Russian-blue?style=for-the-badge&logo=googletranslate&logoColor=white" alt="Bot language: Russian">
</p>

> 🇷🇺 **Note:** the bot's interface and all replies are in **Russian**. This README is written in English for wider GitHub visibility, but no English localization exists in the bot itself.

---

## 📌 About

DetectiveBot is a Telegram bot built with **aiogram 3.x** that parses shared contacts and stores them in a local **aiosqlite** database. Using the **phonenumbers** library, it extracts the contact's country and mobile operator, then returns a clean summary card to the user.

The database is created automatically  — no manual setup required beyond the bot token.

> All user-facing text (messages, prompts, error messages) is hardcoded in Russian in `main.py` and `utils.py`. If you want an English version, you'll need to translate the strings passed to `message.answer(...)` / `message.reply(...)` and the constants in `utils.py`.

## Features

| Command | Alias | Description |
|---|---|---|
| `/start` | `start` | Greets a returning user, or asks a new user to register by sharing their contact. |
| `/help` | `help` | Shows usage instructions and how to restart the bot. |
| `/checkuser` | `checkuser` | Prompts you to share a contact so the bot can look it up (the bot's main feature). |
| `/share` | `share` | Sends a QR code and link so you can invite friends to the bot. |
| `/admin` | `admin` | Admin-only. Lets the bot owner (matched against `ADMIN_ID`) broadcast an ad to every registered user. |

## How It Works

### Registration & contact lookup

When a user shares a contact, the bot runs through the following logic:

1. **Is the sender registered?** (`user_check` in `data.py`)
2. **Is the shared contact the sender's own contact?**
   - ✅ **Yes, and the sender is registered** → the bot returns the sender's own saved info.
   - ✅ **Yes, and the sender is *not* registered** → the contact is parsed and saved; this *is* the registration step.
   - ❌ **No, it's someone else's contact, and the sender is not registered** → the bot politely asks the sender to register first by sharing their own contact.
   - ❌ **No, it's someone else's contact, and the sender *is* registered** → the bot checks whether that contact already exists in the database:
     - **Already in the database** → the saved record is returned (`get_user` in `data.py`).
     - **Not in the database yet** → the number is parsed with `phonenumbers` (`search_user_info`), the new contact is saved (`add_user`), and the parsed info is returned.

### Broadcasting an ad (`/admin`)

1. The bot asks the admin for the ad text.
2. The bot asks for a link to attach.
3. The message is sent to every user in the database with an inline **"Learn More"** button linking out. Users who have blocked the bot are skipped gracefully.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/OAzizjon/DetectiveBot.git
cd DetectiveBot
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
BOT_TOKEN="345676543sdr3"   # Get this from @BotFather
ADMIN_ID="1234567"          # Get this from @GetMyIDo_Bot — the code converts it to int automatically
```

The `users` table is created automatically on first launch — no manual database setup needed.

## 📁 Project Structure

```
DetectiveBot/
│
├── photo/                   # Images used by the bot (QR code, etc.)
│
├── .env                      # Environment variables (bot token, admin id) — not committed
├── .gitignore                # Excludes .env, app.log, user_data.db, __pycache__/
│
├── main.py                   # Core of the project
├── data.py                   # Database logic (aiosqlite operations)
├── mykeyboard.py              # Reply & inline keyboards
├── utils.py                   # Shared constants & logging helpers
│
├── user_data.db                # SQLite database (auto-generated, not committed)
├── app.log                      # Runtime logs — useful for debugging errors
│
├── requirements.txt              # Project dependencies
└── README.md                     # You are here 👋
```

## Logging

All actions and errors are logged to `app.log` (DEBUG level) and mirrored to the console at INFO level, making it easy to trace what each user did and diagnose failures.

## Contributing

Issues and pull requests are welcome. If you find a bug or have an idea for a feature, feel free to open an issue.

## License
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
