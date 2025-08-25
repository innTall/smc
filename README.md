# SMC Bot — Stage 1 (Fractals & Breakouts)

## Overview
This bot detects fractal breakouts (Sweep & Confirmation) in real time from BingX WebSocket data and sends alerts to Telegram.

### Stage 1 Features
- Connects to BingX WebSocket with auto-reconnect
- Detects fractals of length N (default 5; odd only)
- Classifies **normal** vs **broken** fractals
- Detects **Sweep** and **Confirmation** breakouts strictly after candle close
- One-shot per fractal (UID persistence across restarts)
- Sends alerts to Telegram
- Configurable via `config.json` and Telegram `/set` commands

### Next Stages
- Divergence (RSI / AO)
- Imbalance detection
- BOS (Break of Structure)

