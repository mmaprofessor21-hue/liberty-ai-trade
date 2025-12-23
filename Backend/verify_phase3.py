import asyncio
import websockets
import json
import logging

logger = logging.getLogger(__name__)


async def test_websocket():
    uri = "ws://localhost:8080/ws/market_data"
    logger.info(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            logger.info("Connected! Waiting for messages...")
            for i in range(5):
                message = await websocket.recv()
                data = json.loads(message)
                logger.info(f"Received [{i+1}/5]: {data}")
            logger.info("Test passed: Received 5 messages.")
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        logger.info("Ensure the backend server is running in a separate terminal: uvicorn main:app --reload")


if __name__ == "__main__":
    asyncio.run(test_websocket())
