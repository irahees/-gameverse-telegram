# GameVerse — Telegram Mini App + Offline PWA

GameVerse is a mobile-first mini-game hub. It works as a Telegram Mini App and can also be installed from a supported browser as a standalone PWA.

## Categories and included playable games

- **Two players:** Tic-Tac-Toe, Connect Four, Reaction Duel, Tap Racer (local same-device play)
- **Adventure:** Maze Quest, Snake Run
- **Racing:** Tap Racer (solo and local two-player modes)
- **Puzzle:** 2048, Memory Match, Maze Quest
- **Anti-stress:** Bubble Pop (no timer or pressure), Color Flow

Games are local/offline experiences. The two-player games currently use the same device; online matchmaking and remote multiplayer are not included.

## Offline support

- The service worker caches the app shell, manifest, icon and health endpoint.
- After the first successful online visit and cache installation, the standalone PWA can reopen offline.
- Open the site once while online, wait for the offline-ready message, then use the browser's **Install app** or **Add to Home screen** option.
- A Telegram Mini App still needs Telegram and an internet connection to initially open. For offline play, launch the installed GameVerse PWA from your home screen.

## Run locally

\`\`\`bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`

Open http://127.0.0.1:8000. For service-worker/PWA testing, use localhost or HTTPS.

## Deploy on Render

The existing Render Blueprint remains unchanged. Set \`BOT_TOKEN\` and \`APP_URL\` privately in Render environment variables. Never commit the bot token.

## Current scope

- Local browser games; persistent high scores and cloud saves are not implemented yet.
- No accounts, cloud saves, online rooms, matchmaking, or persistent global leaderboards yet.
- The free Render plan may sleep when idle; the first online visit after sleep may take longer.
