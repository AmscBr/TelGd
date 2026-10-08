import asyncio
import calendar
import datetime
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox

HEAD
api_id = config.api_id
api_hash = config.api_hash
client = TelegramClient('teste', api_id, api_hash)

save_dir = 'C:\\Users\\mauri\\Documents\\Progamacao\\Git\\TelGd\\telegram\\fotos\\26.11.24'

start_date = datetime.datetime(2024, 11, 27, tzinfo=pytz.UTC)
end_date = datetime.datetime(2024, 11, 28, tzinfo=pytz.UTC)

async def download_photos(max_messages=2000, expected_photos=70):
    
    await client.start()
    photos_downloaded = 0

    async for message in client.iter_messages(-1001456659134, limit=max_messages):
        
        if message.photo and start_date <= message.date.astimezone(pytz.UTC) <= end_date:

import pytz
from telethon import TelegramClient

import config

# ----------------------------- CONFIGURAÇÕES -----------------------------
CHAT_ID = -1001456659134
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fotos')
TZ = pytz.timezone('America/Sao_Paulo')  # fuso usado para definir "o dia" de cada foto
SESSION_NAME = 'teste'
HORA_CORTE = 6  # o "dia" vai das 06:00 até as 05:59 do dia seguinte
# --------------------------------------------------------------------------


def limites_do_mes(ano, mes):
    """Retorna (início, fim) do mês em UTC, usando a hora de corte."""
    inicio_local = TZ.localize(datetime.datetime(ano, mes, 1, HORA_CORTE))
    if mes == 12:
        fim_local = TZ.localize(datetime.datetime(ano + 1, 1, 1, HORA_CORTE))
    else:
        fim_local = TZ.localize(datetime.datetime(ano, mes + 1, 1, HORA_CORTE))
    return inicio_local.astimezone(pytz.UTC), fim_local.astimezone(pytz.UTC)


def formatar_data(dt):
    return dt.strftime('%d/%m/%Y %H:%M') if dt else 'nenhuma'


def escrever_log(pasta_mes, ano, mes, contagem, mensagens_lidas, mais_recente, mais_antiga):
    """Cria/atualiza o log.txt na pasta do mês com o resumo de cada dia."""
    linhas = [
        f"Log de download - {mes:02d}/{ano}",
        f"Gerado em: {datetime.datetime.now(TZ).strftime('%d/%m/%Y %H:%M:%S')}",
        f"Mensagens lidas no mês: {mensagens_lidas}",
        f"Mensagem mais recente lida: {formatar_data(mais_recente)}",
        f"Mensagem mais antiga lida: {formatar_data(mais_antiga)}",
        "",
    ]

    total_fotos = 0
    dias_com_fotos = 0
    for dia, c in contagem.items():
        total_dia = c["novas"] + c["existentes"]
        if total_dia == 0 and c["erros"] == 0:
            linhas.append(f"Dia {dia:02d}: sem fotos")
            continue

        total_fotos += total_dia
        if total_dia:
            dias_com_fotos += 1
        texto = f"Dia {dia:02d}: {total_dia} fotos ({c['novas']} novas, {c['existentes']} já existiam)"
        if c["erros"]:
            texto += f" - {c['erros']} com erro"
        linhas.append(texto)

    linhas += ["", f"Total: {total_fotos} fotos em {dias_com_fotos} dias"]

    with open(os.path.join(pasta_mes, "log.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")


async def baixar_fotos_do_mes(ano, mes, progresso=None):
    """Baixa todas as fotos do mês e salva em uma pasta para cada dia.

    Estrutura: BASE_DIR / AAAA-MM / AAAA-MM-DD / <id_da_mensagem>.jpg
    Também gera BASE_DIR / AAAA-MM / log.txt com o resumo de cada dia.
    Fotos já baixadas são puladas, então dá para rodar de novo sem duplicar.
    """
    inicio_utc, fim_utc = limites_do_mes(ano, mes)
    pasta_mes = os.path.join(BASE_DIR, f"{mes:02d}.{ano}")
    os.makedirs(pasta_mes, exist_ok=True)

    dias_no_mes = calendar.monthrange(ano, mes)[1]
    contagem = {d: {"novas": 0, "existentes": 0, "erros": 0} for d in range(1, dias_no_mes + 1)}

    mensagens_lidas = 0
    mais_recente = None
    mais_antiga = None
    novas = 0

    async with TelegramClient(SESSION_NAME, config.api_id, config.api_hash) as client:
        # Começa 1 dia depois do fim do mês e descarta o excesso manualmente,
        # assim o último dia do mês nunca fica de fora por causa do limite do offset.
        offset = fim_utc + datetime.timedelta(days=1)

        async for message in client.iter_messages(CHAT_ID, offset_date=offset):
            data_utc = message.date.astimezone(pytz.UTC)

            if data_utc >= fim_utc:
                continue  # já é do mês seguinte
            if data_utc < inicio_utc:
                break  # passou do início do mês: acabou

            data_local = data_utc.astimezone(TZ)
            mensagens_lidas += 1
            if mais_recente is None:
                mais_recente = data_local
            mais_antiga = data_local

            if not message.photo:
                continue

            data_logica = data_local - datetime.timedelta(hours=HORA_CORTE)
            dia = data_logica.day
            pasta_dia = os.path.join(pasta_mes, data_logica.strftime('%d.%m.%Y'))
            os.makedirs(pasta_dia, exist_ok=True)

            caminho = os.path.join(pasta_dia, f"{message.id}.jpg")
            if os.path.exists(caminho):
                contagem[dia]["existentes"] += 1
                continue

 87beb49 (Atualização do script data data_telegram.py, e outras melhorias)
            try:
                await message.download_media(file=caminho)
                contagem[dia]["novas"] += 1
                novas += 1
                if progresso:
                    progresso(f"Baixando... {novas} fotos (dia {dia:02d})")
            except Exception as e:
                contagem[dia]["erros"] += 1
                print(f"Erro ao baixar foto {message.id}: {e}")

HEAD
        if photos_downloaded >= expected_photos:
            break

    escrever_log(pasta_mes, ano, mes, contagem, mensagens_lidas, mais_recente, mais_antiga)
87beb49 (Atualização do script data data_telegram.py, e outras melhorias)

    puladas = sum(c["existentes"] for c in contagem.values())
    erros = sum(c["erros"] for c in contagem.values())
    por_dia = {d: c["novas"] for d, c in contagem.items() if c["novas"]}
    return novas, puladas, erros, por_dia

HEAD
def iniciar_download():
    
    try:
        total_fotos = asyncio.run(download_photos())
        messagebox.showinfo("Sucesso", f"Download concluído! Total de fotos: {total_fotos}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")



# ------------------------------- INTERFACE --------------------------------
87beb49 (Atualização do script data data_telegram.py, e outras melhorias)
janela = tk.Tk()
janela.title("Downloader de Fotos do Telegram")

hoje = datetime.date.today()

frame = ttk.Frame(janela, padding=15)
frame.pack()

HEAD

ttk.Label(frame, text="Mês:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
combo_mes = ttk.Combobox(frame, values=list(range(1, 13)), width=5, state="readonly")
combo_mes.set(hoje.month)
combo_mes.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="Ano:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
combo_ano = ttk.Combobox(
    frame, values=list(range(hoje.year - 5, hoje.year + 1)), width=7, state="readonly"
)
combo_ano.set(hoje.year)
combo_ano.grid(row=0, column=3, padx=5, pady=5)

status = tk.StringVar(value="Escolha o mês e clique em Iniciar Download.")
ttk.Label(frame, textvariable=status).grid(row=1, column=0, columnspan=4, pady=10)

botao = ttk.Button(frame, text="Iniciar Download")
botao.grid(row=2, column=0, columnspan=4, pady=5)


def atualizar_status(texto):
    # Chamado a partir da thread de download: agenda a atualização na thread da interface
    janela.after(0, lambda: status.set(texto))


def finalizar(resultado=None, erro=None):
    botao.config(state="normal")
    if erro:
        status.set("Erro durante o download.")
        messagebox.showerror("Erro", f"Ocorreu um erro: {erro}")
        return

    novas, puladas, erros, por_dia = resultado
    status.set(f"Concluído! {novas} novas fotos.")
    resumo = (
        f"Download concluído!\n\n"
        f"Fotos novas: {novas}\n"
        f"Já existiam (puladas): {puladas}\n"
        f"Erros: {erros}\n"
        f"Dias com fotos novas: {len(por_dia)}\n\n"
        f"O resumo por dia está no log.txt da pasta do mês."
    )
    messagebox.showinfo("Sucesso", resumo)


def trabalho(ano, mes):
    try:
        resultado = asyncio.run(baixar_fotos_do_mes(ano, mes, atualizar_status))
        janela.after(0, lambda r=resultado: finalizar(resultado=r))
    except Exception as e:
        janela.after(0, lambda err=e: finalizar(erro=err))


def iniciar_download():
    ano = int(combo_ano.get())
    mes = int(combo_mes.get())
    botao.config(state="disabled")
    status.set("Conectando ao Telegram...")
    # Roda em outra thread para a janela não travar durante o download
    threading.Thread(target=trabalho, args=(ano, mes), daemon=True).start()


botao.config(command=iniciar_download)
87beb49 (Atualização do script data data_telegram.py, e outras melhorias)
janela.mainloop()
