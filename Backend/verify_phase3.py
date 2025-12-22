import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8080/ws/market_data"
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected! Waiting for messages...")
            for i in range(5):
                message = await websocket.recv()
                data = json.loads(message)
                print(f"Received [{i+1}/5]: {data}")
            print("Test passed: Received 5 messages.")
    except Exception as e:
        print(f"Connection failed: {e}")
        print("Ensure the backend server is running in a separate terminal: uvicorn main:app --reload")

if __name__ == "__main__":
    # Note: This script assumes the server is already running.
    # Since I cannot run the server in background easily and run this client in the same shell synchronously,
    # I will try to run this. If it fails due to no server, I might need a different approach 
    # (starting server in background process using run_command).
    asyncio.run(test_websocket())
