import config
import datetime
from telethon import TelegramClient
import pytz
import tkinter as tk
from tkinter import messagebox
import asyncio

api_id = config.api_id
api_hash = config.api_hash

# 1. MUDANÇA DE SESSÃO E CONEXÃO: 
# Novo nome de sessão ('downloader_final') e 'connection_retries=None' para estabilidade.
client = TelegramClient('downloader_final', api_id, api_hash, connection_retries=None)

save_dir = 'C:\\Users\\sousa\\Documents\\progamacao\\git\\TelGd\\telegram\\fotos\\06.11.25'

# As datas em UTC estão corretas
start_date = datetime.datetime(2025, 11, 7, tzinfo=pytz.UTC)
end_date = datetime.datetime(2025, 11, 8, tzinfo=pytz.UTC)

async def download_photos(max_messages=2000, expected_photos=70):
    
    await client.start()
    photos_downloaded = 0

    # 2. OTIMIZAÇÃO DE BUSCA: Usando offset_date e reverse=True.
    # Isso faz a busca começar na data de início e ir para a frente, garantindo velocidade.
    async for message in client.iter_messages(
        -1001456659134, 
        limit=max_messages, 
        offset_date=start_date, # Começa a busca nesta data
        reverse=True # Busca para frente no tempo
    ):
        
        # 3. CONDIÇÃO DE PARADA OTIMIZADA: Para quando atingir ou ultrapassar a data final.
        if message.date.astimezone(pytz.UTC) >= end_date:
            break
        
        if message.photo:
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