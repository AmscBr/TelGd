import config
import datetime
from telethon import TelegramClient
import pytz
import tkinter as tk
from tkinter import messagebox
import asyncio

# Configurações da API do Telegram
api_id = config.api_id
api_hash = config.api_hash
client = TelegramClient('teste', api_id, api_hash)

# Diretório para salvar as fotos
save_dir = 'C:\\Users\\sousa\\Documents\\Progamação\\GaragemDown\\fotos\\02.09.24'

# Data de hoje com fuso horário UTC
start_date = datetime.datetime(2024, 9, 3, tzinfo=pytz.UTC)
end_date = datetime.datetime(2024, 9, 4, tzinfo=pytz.UTC)

async def download_photos(max_messages=100):  # Adiciona um parâmetro para limitar o número de mensagens
    await client.start()
    photos_downloaded = 0  # Contador para o número de fotos baixadas
    async for message in client.iter_messages(-1001456659134, limit=max_messages):  # Limita o número de mensagens
        message_date = message.date.astimezone(pytz.UTC)
        if start_date <= message_date <= end_date:
            if message.photo:
                file_path = await message.download_media(file=save_dir)
                print(f'Foto salva em {file_path}')
                photos_downloaded += 1  # Incrementa o contador de fotos

    # Desconecta o cliente do Telegram após o download
    await client.disconnect()
    
    return photos_downloaded  # Retorna o número de fotos baixadas

def show_success_message(photos_downloaded):
    messagebox.showinfo("Download Concluído", f"{photos_downloaded} fotos foram baixadas com sucesso.")
    root.destroy()   

def start_download():
    download_button.config(state=tk.DISABLED)  
    asyncio.run(download_and_notify())

async def download_and_notify():
    photos_downloaded = await download_photos(max_messages=50) 
    root.after(0, show_success_message, photos_downloaded)  

root = tk.Tk()
root.title("Download de fotos do Telegram")

download_button = tk.Button(root, text="Baixar Fotos", command=start_download)
download_button.pack(pady=20)

root.mainloop()
