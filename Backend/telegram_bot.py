# P25-06-04_14-47-51
import aiohttp

async def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as resp:
            return await resp.json()
