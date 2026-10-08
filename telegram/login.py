import config
from telethon import TelegramClient
import asyncio

api_id = config.api_id
api_hash = config.api_hash

async def main():
    # Cria o cliente, que usará o arquivo de sessão 'teste.session'
    client = TelegramClient('teste', api_id, api_hash) 
    
    # Inicia a sessão. Se 'teste.session' não existir, ele pedirá as credenciais no terminal.
    await client.start() 
    
    print("Sessão iniciada com sucesso! O arquivo 'teste.session' foi criado.")
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())