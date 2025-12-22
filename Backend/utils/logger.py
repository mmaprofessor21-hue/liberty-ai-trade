import logging
import json
import time
from datetime import datetime
import os

# Create logs directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

class StructuredLogger:
    def __init__(self, name="LibertyAI"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # File Handler (Immutable Ledger style - Append Only)
        filename = f"{LOG_DIR}/trade_ledger_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        handler = logging.FileHandler(filename)
        
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Console Handler
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        self.logger.addHandler(console)

    def log_event(self, event_type: str, details: dict):
        """
        Logs an event in strict JSON format.
        """
        entry = {
            "timestamp": time.time(),
            "iso_time": datetime.now().isoformat(),
            "type": event_type,
            "details": details
        }
        self.logger.info(json.dumps(entry))

    def log_trade(self, signal, amount, result):
        self.log_event("TRADE_EXECUTION", {
            "symbol": signal.symbol,
            "action": signal.type,
            "amount": amount,
            "strategy": signal.strategy,
            "ai_confidence": signal.ai_confidence,
            "result": result
        })

    def log_security(self, check: str, status: str, details: str):
        self.log_event("SECURITY_CHECK", {
            "check": check,
            "status": status,
            "details": details
        })

system_logger = StructuredLogger()
