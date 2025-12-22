import asyncio
import random
import time
from typing import List, Dict

class DataEngine:
    def __init__(self, allow_demo: bool = False):
        self.listeners = []
        self.running = False
        self.current_price = 150.0
        # When False, the engine will NOT emit mock market ticks.
        # This prevents fake signals unless demo mode is explicitly enabled.
        self.allow_demo = allow_demo

    async def start_streaming(self):
        """Start the data engine loop.

        If `allow_demo` is False the engine will NOT emit mock market ticks
        and will instead broadcast DATA_UNAVAILABLE messages so the UI
        can display 'Unavailable' rather than simulated values.
        """
        self.running = True
        print("Starting Data Engine Stream...")
        while self.running:
            if not self.allow_demo:
                # Inform listeners that market data is unavailable
                payload = {
                    "type": "DATA_UNAVAILABLE",
                    "reason": "demo_disabled",
                    "timestamp": time.time(),
                }
                for queue in self.listeners:
                    await queue.put(payload)
                await asyncio.sleep(5)
                continue

            # Generate mock candle/tick when demo allowed
            change = random.uniform(-0.5, 0.5)
            self.current_price += change

            payload = {
                "type": "TICK",
                "symbol": "SOL/USDC",
                "price": round(self.current_price, 2),
                "timestamp": time.time(),
                "indicators": {
                    "EMA_9": round(self.current_price * 0.99, 2),
                    "RSI_14": round(random.uniform(30, 70), 2)
                }
            }

            # Randomly inject a trade event
            if random.random() < 0.1:  # 10% chance
                trade_payload = {
                    "type": "TRADE_EVENT",
                    "symbol": "SOL/USDC",
                    "action": "BUY" if random.random() > 0.5 else "SELL",
                    "price": round(self.current_price, 2),
                    "amount": round(random.uniform(0.1, 1.0), 2),
                    "strategy": "MOCK_AI",
                }
                # Send trade event immediately
                for queue in self.listeners:
                    await queue.put(trade_payload)

            # Broadcast tick to all websocket queues
            for queue in self.listeners:
                await queue.put(payload)

            await asyncio.sleep(1)  # 1 sec tick for demo

    def stop(self):
        self.running = False

    def subscribe(self):
        queue = asyncio.Queue()
        self.listeners.append(queue)
        return queue

    def unsubscribe(self, queue):
        if queue in self.listeners:
            self.listeners.remove(queue)

data_engine = DataEngine()
