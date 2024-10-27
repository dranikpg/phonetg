from telethon import TelegramClient, events, sync
import asyncio

api_id = 27979506
api_hash = '2666f30330c0333d93c5eae2c67d67b3'


async def main():
    client = TelegramClient('nokiabot0925', api_id, api_hash)

    await client.start()
    print("started")

    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        print(await client.get_messages(dialog, limit=10))
        print()


asyncio.run(main())
