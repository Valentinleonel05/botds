# bot.py - Archivo principal del bot de Discord
# Este archivo solo inicializa el bot y carga los sistemas/comandos globales.

import discord
from discord.ext import commands
from municipio.municipio_commands import setup_municipio_commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Cargar comandos del municipio (y otros sistemas en el futuro)
setup_municipio_commands(bot)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Comandos slash sincronizados: {len(synced)}')
    except Exception as e:
        print(f'Error al sincronizar comandos: {e}')

# Inicia el bot (reemplaza 'TU_TOKEN_AQUI' por tu token real)
bot.run('MTQ5Mzc5OTcwMTM3NDMwNDI3Nw.GFfOpo.QUDxERHLBGNr3n2Rxn7mfHpTIGnisnPzlZznGo')