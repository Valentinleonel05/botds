# municipio_commands.py - Comandos y vistas del sistema de identidad y otros sistemas del municipio
import discord
from discord.ext import commands
from discord import Interaction, Embed, ButtonStyle
from discord.ui import View, Button, Modal, TextInput
from municipio.identidad import IdentidadManager
import datetime

identidad_manager = IdentidadManager()

# Vista del menú principal del municipio
class MenuMunicipioView(View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    @discord.ui.button(label="DNIs", style=ButtonStyle.blurple, custom_id="menu_dnis")
    async def dnis(self, interaction: Interaction, button: Button):
        if str(interaction.user.id) != str(self.user_id):
            await interaction.response.send_message("No puedes usar este botón.", ephemeral=True)
            return
        embed = Embed(
            title="🪪 Sistema de DNIs",
            description="Gestión de documentos de identidad.\n\n**¿Qué deseas hacer?**",
            color=0x42c2ff
        )
        await interaction.response.send_message(embed=embed, view=MenuDNIView(self.user_id), ephemeral=True)

    @discord.ui.button(label="📄 Licencias", style=ButtonStyle.success, custom_id="menu_licencias")
    async def licencias(self, interaction: Interaction, button: Button):
        if str(interaction.user.id) != str(self.user_id):
            await interaction.response.send_message("No puedes usar este botón.", ephemeral=True)
            return
        embed = Embed(
            title="Licencias",
            description="El sistema de licencias está en desarrollo.",
            color=0x27ae60
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Modal para crear identidad
class CrearIdentidadModal(Modal, title="Crear DNI"):
    nombre = TextInput(label="Nombre", placeholder="Tu nombre", required=True, max_length=30)
    apellido = TextInput(label="Apellido", placeholder="Tu apellido", required=True, max_length=30)
    genero = TextInput(label="Género (Masculino/Femenino/Otro)", placeholder="Selecciona tu género", required=True, max_length=15)
    fecha_nacimiento = TextInput(label="Fecha de nacimiento (DD/MM/AAAA)", placeholder="Ej: 19/01/2000", required=True, max_length=10)
    nacionalidad = TextInput(label="Nacionalidad", placeholder="Ej: Argentina", required=True, max_length=30)

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    async def on_submit(self, interaction: Interaction):
        # Validar fecha de nacimiento
        try:
            fecha = datetime.datetime.strptime(str(self.fecha_nacimiento), "%d/%m/%Y")
            hoy = datetime.datetime.now()
            edad = (hoy - fecha).days // 365
            if edad > 100:
                await interaction.response.send_message("La edad máxima permitida es 100 años.", ephemeral=True)
                return
        except Exception:
            await interaction.response.send_message("Fecha de nacimiento inválida. Usa el formato DD/MM/AAAA.", ephemeral=True)
            return
        # Validar género
        genero_valido = str(self.genero).strip().lower() in ["masculino", "femenino", "otro"]
        if not genero_valido:
            await interaction.response.send_message("El género debe ser Masculino, Femenino u Otro.", ephemeral=True)
            return
        # Crear identidad
        creado = identidad_manager.crear_identidad(
            str(interaction.user.id),
            str(self.nombre),
            str(self.apellido),
            str(self.genero),
            str(self.fecha_nacimiento),
            str(self.nacionalidad)
        )
        if creado:
            await interaction.response.send_message("DNI creado correctamente.", ephemeral=True)
        else:
            await interaction.response.send_message("Ya tienes un DNI registrado.", ephemeral=True)

# Vista del menú de DNIs
class MenuDNIView(View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    @discord.ui.button(label="Crear DNI", style=ButtonStyle.green, custom_id="crear_dni")
    async def crear_dni(self, interaction: Interaction, button: Button):
        if str(interaction.user.id) != str(self.user_id):
            await interaction.response.send_message("No puedes usar este botón.", ephemeral=True)
            return
        identidad = identidad_manager.obtener_identidad(str(interaction.user.id))
        if identidad:
            await interaction.response.send_message("Ya tienes un DNI registrado. No puedes crear otro.", ephemeral=True)
            return
        await interaction.response.send_modal(CrearIdentidadModal(self.user_id))

    @discord.ui.button(label="Ver DNI", style=ButtonStyle.blurple, custom_id="ver_dni")
    async def ver_dni(self, interaction: Interaction, button: Button):
        if str(interaction.user.id) != str(self.user_id):
            await interaction.response.send_message("No puedes usar este botón.", ephemeral=True)
            return
        identidad = identidad_manager.obtener_identidad(str(interaction.user.id))
        if identidad:
            embed = Embed(title="🪪 DNI Ciudadano", color=0x3498db)
            embed.add_field(name="Nombre", value=identidad['nombre'], inline=True)
            embed.add_field(name="Apellido", value=identidad['apellido'], inline=True)
            embed.add_field(name="Género", value=identidad['genero'], inline=True)
            embed.add_field(name="Fecha de Nacimiento", value=identidad['fecha_nacimiento'], inline=True)
            embed.add_field(name="Nacionalidad", value=identidad['nacionalidad'], inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("No tienes un DNI registrado.", ephemeral=True)

def setup_municipio_commands(bot):
    @bot.tree.command(name="municipio", description="Accede al sistema digital municipal.")
    async def municipio_command(interaction: Interaction):
        embed = Embed(
            title="🏛️ Sistema Municipal",
            description="Bienvenido al sistema digital municipal.\n\n**Selecciona una opción:**\nMunicipalidad",
            color=0xf1c40f
        )
        await interaction.response.send_message(embed=embed, view=MenuMunicipioView(interaction.user.id), ephemeral=True)
