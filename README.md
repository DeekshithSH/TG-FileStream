# TG-FileStream

**TG-FileStream** is a lightweight web server and Telegram client that acts as a proxy between Telegram servers and HTTP clients, allowing direct downloads of Telegram media files via HTTP.

---

## 🔁 Project Background

This project is a **successor** to  
👉 [DeekshithSH/TG-FileStreamBot](https://github.com/DeekshithSH/TG-FileStreamBot),  
which itself was a fork of  
👉 [EverythingSuckz/TG-FileStreamBot](https://github.com/EverythingSuckz/TG-FileStreamBot).

The original Python version became inactive after EverythingSuckz rewrote the project in Golang. Instead of continuing from the older Python codebase, this project is a fresh rewrite using [Telethon](https://github.com/LonamiWebs/Telethon) with a minimal approach.

> 📌 Check out [TODO.md](./TODO.md) for the latest development progress and planned features.

---

## 🚀 Features

- Download Telegram media via HTTP links  
- Fast, concurrent chunked downloading  
- Minimal setup, no database required

---

## 🛠️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/DeekshithSH/TG-FileStream.git
cd TG-FileStream
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

Store the required environment variables in a `.env` file:

```env
API_ID=1234567
API_HASH=1a2b3c4d5e6f7g8h9i0jklmnopqrstuv
BOT_TOKEN=1234567890:AAExampleBotTokenGeneratedHere
BIN_CHANNEL=-1002605638795
HOST=0.0.0.0
PORT=8080
PUBLIC_URL=http://127.0.0.1:8080
```

### 4. Run the server

```bash
python3 -m tgfs
```

---

## ⚙️ Environment Variables

| Variable             | Required/Default       | Description                                                                  |
| -------------------- | ---------------------- | ---------------------------------------------------------------------------- |
| `API_ID`             | ✅                     | App ID from [my.telegram.org](https://my.telegram.org)                       |
| `API_HASH`           | ✅                     | API hash from [my.telegram.org](https://my.telegram.org)                     |
| `BOT_TOKEN`          | ✅                     | Bot token from [@BotFather](https://t.me/BotFather)                          |
| `BIN_CHANNEL`        | ✅                     | Channel ID where files sent to the bot are stored                            |
| `HOST`               | `0.0.0.0`              | Host address to bind the server (default: `0.0.0.0`)                         |
| `PORT`               | `8080`                 | Port to run the server on (default: `8080`)                                  |
| `PUBLIC_URL`         | `https://0.0.0.0:8080` | Public-facing URL used to generate download links                            |
| `CONNECTION_LIMIT`   | `20`                   | Number of connections to create per DC for a single client                   |
| `CACHE_SIZE`         | `128`                  | Number of file info objects to cache                                         |
| `TIMEOUT_SECONDS`    | `30`                   | Number of seconds to wait after sending a `GetFileRequest` before timing out |
| `DOWNLOAD_PART_SIZE` | `1048576 (1MB)`        | Number of bytes to request in a single chunk                                 |
| `PREFETCH_COUNT`     | `2`                    | Number of chunks to request in advance                                       |
| `NO_UPDATE`          | `False`                | Whether to reply to messages sent to the bot (True to disable replies)       |



- `MULTI_TOKENx`: Use Multiple Telegram Clients when downloading files to avoid flood wait, Replace x with Number

example:
```
MULTI_TOKEN1=1234567890:AAExampleBotTokenGeneratedHere
MULTI_TOKEN2=0987654321:AAExampleBotTokenGeneratedHere
MULTI_TOKEN3=5432167890:AAExampleBotTokenGeneratedHere
```

---

## 📂 Usage

Once the server is running, you can:

- Access Telegram media files via HTTP:

```
http://{PUBLIC_URL}/{message_id}/{filename}
```

- Or simply send a file to your bot, and it will respond with a download link.

This will stream the file directly from Telegram servers to the client.

---

## 💡 Credits

- **Deekshith SH** – Me (aka **SpringsFern**, **GatheredAtom696**)
- **Tulir** – Original author of [`tg-filestream`](https://github.com/tulir/tg-filestream), whose code inspired this project and is referenced in `paralleltransfer.py`

---
