# Sistema de Identidad - Municipio
# Este archivo gestionará la identidad de los ciudadanos y servirá como base para conectar los demás sistemas.

import sqlite3
from typing import Optional, Dict, Any

DB_PATH = 'municipio/identidad.db'

class IdentidadManager:
    def __init__(self, db_path: str = DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS ciudadanos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    discord_id TEXT UNIQUE,
                    nombre TEXT,
                    apellido TEXT,
                    genero TEXT,
                    fecha_nacimiento TEXT,
                    nacionalidad TEXT,
                    hijos TEXT,
                    bienes TEXT,
                    cuentas_bancarias TEXT
                )
            ''')

    def crear_identidad(self, discord_id: str, nombre: str, apellido: str, genero: str, fecha_nacimiento: str, nacionalidad: str) -> bool:
        try:
            with self.conn:
                self.conn.execute(
                    'INSERT INTO ciudadanos (discord_id, nombre, apellido, genero, fecha_nacimiento, nacionalidad, hijos, bienes, cuentas_bancarias) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (discord_id, nombre, apellido, genero, fecha_nacimiento, nacionalidad, '', '', '')
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def obtener_identidad(self, discord_id: str) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM ciudadanos WHERE discord_id = ?', (discord_id,))
        row = cur.fetchone()
        if row:
            return {
                'id': row[0],
                'discord_id': row[1],
                'nombre': row[2],
                'apellido': row[3],
                'genero': row[4],
                'fecha_nacimiento': row[5],
                'nacionalidad': row[6],
                'hijos': row[7],
                'bienes': row[8],
                'cuentas_bancarias': row[9]
            }
        return None

    # Métodos para editar hijos, bienes, cuentas, etc. se agregarán luego

# Ejemplo de uso:
# identidad = IdentidadManager()
# identidad.crear_identidad('123456', 'Juan', 'Pérez', '2000-01-01')
# print(identidad.obtener_identidad('123456'))
