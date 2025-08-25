from core.candle_store import CandleStore

class SignalEngine:
    def __init__(self, config, telegram):
        """
        config: dict from config.json
        telegram: TelegramClient instance
        """
        self.config = config
        self.telegram = telegram
        self.candles = CandleStore(config["history_limit"])

        # Switch for debugging signals
        self.debug_signals = config["telegram"].get("debug_signals", False)
        
    def handle_candle(self, symbol, interval, candle):
        """
        Update store with new candle and (optionally) send debug signal.
        """
        self.candles.update(symbol, interval, candle)

        # Debug/test mode: send every closed candle to Telegram
        if self.debug_signals and candle["is_closed"]:
            msg = f"📊 {symbol} {interval} closed at {candle['close']}"
            self.telegram.send(msg)

        # Future: fractal detection, breakouts, etc.
        # Example:
        # signals = self.detect_fractals(symbol, interval)
        # for s in signals:
        #     self.telegram.send(s)
        
# python core/signal_engine.py