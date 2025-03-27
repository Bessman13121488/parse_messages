import asyncio
import json

from telegram import Bot

TELEGRAM_BOT_TOKEN = 'your-telegram-bot-token'

def load_json_into_dict(filename):
    result = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            try:
                json_string = line.strip()
                json_string = json_string.replace('\\"', "\\'")
                data = json.loads(json_string)
                result.append(data)
            except json.decoder.JSONDecodeError as e:
                print(e)
    return result


async def send_message(message, user):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await  bot.send_message(chat_id=user['telegram_id'], text=message)
    except Exception:
        print("Sending message")


def found_keywords(message, keywords):
    return any(keyword.lower() in message.lower() for keyword in keywords)


async def main():
    users = load_json_into_dict("user.json")
    messages = load_json_into_dict("messages.json")
    for message in messages:
        for user in users:
            if found_keywords(message.get("message_text"), user.get('keywords')):
                await send_message(message, user)

    print("Обработка завершена!")


if __name__ == "__main__":
    asyncio.run(main())
