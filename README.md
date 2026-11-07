# GameVerse — Telegram Mini App

A mobile-first Telegram game hub. This repository is separate from any other bot projects.

## Included starter games
- Snake — single-player arcade
- 2048 — number puzzle
- Tic-Tac-Toe — two players on one device
- Bubble Pop — relaxing tap game

The app is built with FastAPI and a static HTML/CSS/JavaScript frontend. It uses the Telegram Mini Apps SDK when opened inside Telegram and also works in a normal browser.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Open http://127.0.0.1:8000.

## Deploy on Render
1. Create a new **Blueprint** in Render and select this repository.
2. Render reads `render.yaml` and creates the web service.
3. In the service environment, set:
   - `BOT_TOKEN`: token from BotFather
   - `APP_URL`: the public HTTPS URL of the Render service, e.g. `https://gameverse-telegram.onrender.com`
4. Redeploy. The app configures the Telegram webhook on startup.
5. In BotFather, optionally set the bot's menu button to a web app using the same HTTPS URL.

Keep the bot token private. Never commit it to GitHub.

## Current scope
This is the first playable foundation. Online multiplayer rooms, matchmaking, accounts, and persistent leaderboards are not implemented yet. The free Render plan may sleep when idle, so the first request after inactivity can take longer.
