from telethon import TelegramClient
import config

api_id = config.api_id
api_hash = config.api_hash
client = TelegramClient('teste', api_id, api_hash)

async def main():

    me = await client.get_me()

    async for message in client.iter_messages('@mariojrb2k'):
                                              print(message.id, message.text)

                                              if message.photo:
                                                  path = await message.download_media()
                                                  print('File save to', path)

with client:
    client.loop.run_until_complete(main())
