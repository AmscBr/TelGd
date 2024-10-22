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
save_dir = 'C:\\Users\\sousa\\Documents\\Progamacao\\TelGd\\fotos\\12.10.24'

# Data com fuso horário UTC (intervalo necessário)
start_date = datetime.datetime(2024, 10, 13, tzinfo=pytz.UTC)
end_date = datetime.datetime(2024, 10, 14, tzinfo=pytz.UTC)

async def download_photos(max_messages=1000, expected_photos=49):
    """Baixa fotos de um grupo no Telegram no intervalo de tempo especificado."""
    await client.start()
    photos_downloaded = 0

    async for message in client.iter_messages(-1001456659134, limit=max_messages):
        # Filtrar apenas mensagens com fotos e dentro do intervalo de tempo
        if message.photo and start_date <= message.date.astimezone(pytz.UTC) <= end_date:
            try:
                file_path = await message.download_media(file=save_dir)
                photos_downloaded += 1
            except Exception as e:
                print(f"Erro ao baixar foto: {e}")

        # Interromper a busca quando o número esperado de fotos for alcançado
        if photos_downloaded >= expected_photos:
            break

    return photos_downloaded

def iniciar_download():
    """Inicia o download das fotos ao clicar no botão."""
    try:
        total_fotos = asyncio.run(download_photos())
        messagebox.showinfo("Sucesso", f"Download concluído! Total de fotos: {total_fotos}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Interface gráfica com tkinter
janela = tk.Tk()
janela.title("Downloader de Fotos do Telegram")

label = tk.Label(janela, text="Clique no botão para iniciar o download das fotos.")
label.pack(padx=10, pady=10)

botao = tk.Button(janela, text="Iniciar Download", command=iniciar_download)
botao.pack(padx=10, pady=10)

# Iniciar a interface gráfica
janela.mainloop()
