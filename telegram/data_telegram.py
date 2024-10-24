import config
import datetime
from telethon import TelegramClient
import pytz
import tkinter as tk
from tkinter import messagebox
import asyncio

api_id = config.api_id
api_hash = config.api_hash
client = TelegramClient('teste', api_id, api_hash)

save_dir = 'C:\\Users\\mauri\\Documents\\Progamacao\\Git\\TelGd\\telegram\\fotos\\22.10.24'

start_date = datetime.datetime(2024, 10, 23, tzinfo=pytz.UTC)
end_date = datetime.datetime(2024, 10, 24, tzinfo=pytz.UTC)

async def download_photos(max_messages=1000, expected_photos=70):
    
    await client.start()
    photos_downloaded = 0

    async for message in client.iter_messages(-1001456659134, limit=max_messages):
        
        if message.photo and start_date <= message.date.astimezone(pytz.UTC) <= end_date:
            try:
                file_path = await message.download_media(file=save_dir)
                photos_downloaded += 1
            except Exception as e:
                print(f"Erro ao baixar foto: {e}")

        if photos_downloaded >= expected_photos:
            break

    return photos_downloaded

def iniciar_download():
    
    try:
        total_fotos = asyncio.run(download_photos())
        messagebox.showinfo("Sucesso", f"Download concluído! Total de fotos: {total_fotos}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

janela = tk.Tk()
janela.title("Downloader de Fotos do Telegram")

label = tk.Label(janela, text="Clique no botão para iniciar o download das fotos.")
label.pack(padx=10, pady=10)

botao = tk.Button(janela, text="Iniciar Download", command=iniciar_download)
botao.pack(padx=10, pady=10)

janela.mainloop()
