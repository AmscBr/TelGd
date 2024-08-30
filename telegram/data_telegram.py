import config
import datetime
from telethon import TelegramClient
import pytz

# Configurações da API do Telegram
api_id = config.api_id
api_hash = config.api_hash
client = TelegramClient('teste', api_id, api_hash)

# Diretório para salvar as fotos
save_dir = 'C:\\Users\\sousa\\Documents\\Progamação\\GaragemDown\\fotos\\28.08.24'

# Data de hoje com fuso horário UTC
start_date = datetime.datetime(2024, 8, 29, tzinfo=pytz.UTC)
end_date = datetime.datetime(2024, 8, 30, tzinfo=pytz.UTC)

async def download_photos():
    await client.start()
    async for message in client.iter_messages(-1001456659134):
        message_date = message.date.astimezone(pytz.UTC)
        if start_date <= message_date <= end_date:
            if message.photo:
                file_path = await message.download_media(file=save_dir)
                print(f'Foto salva em {file_path}')
                
with client:
    client.loop.run_until_complete(download_photos())


