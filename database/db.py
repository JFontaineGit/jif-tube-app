import sqlite3
import pandas as pd
from datetime import datetime

class Database:
    def __init__(self, db_name="jiftube.db"):
        """Inicializa la base de datos y crea las tablas si no existen."""
        self.db_name = db_name
        self.create_tables()

    def create_tables(self):
        """Crea las tablas necesarias si no existen usando un administrador de contexto."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                #Historial de Reproducción
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS historial_reproduccion (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cancion_id TEXT NOT NULL,
                        titulo TEXT NOT NULL,
                        artista TEXT NOT NULL,
                        fecha_reproduccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Playlists
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS playlists (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Relación Playlist-Canciones
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS playlist_canciones (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        playlist_id INTEGER NOT NULL,
                        cancion_id TEXT NOT NULL,
                        FOREIGN KEY (playlist_id) REFERENCES playlists(id)
                    )
                ''')

                # Favoritos
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS favoritos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cancion_id TEXT NOT NULL
                    )
                ''')

                conn.commit()
                print("Tablas creadas exitosamente o ya existían.")

        except sqlite3.Error as e:
            print(f"Error al crear las tablas: {e}")

    def insert_historial(self, cancion_id, titulo, artista):
        """Inserta un registro en el historial de reproducción."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO historial_reproduccion (cancion_id, titulo, artista) VALUES (?, ?, ?)
                ''', (cancion_id, titulo, artista))
                conn.commit()
                print(f"Canción {titulo} añadida al historial.")
        except sqlite3.Error as e:
            print(f"Error al insertar en historial: {e}")

    def insert_playlist(self, nombre):
        """Inserta una playlist en la tabla playlists."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO playlists (nombre) VALUES (?)
                ''', (nombre,))
                conn.commit()
                print(f"Playlist {nombre} creada correctamente.")
        except sqlite3.Error as e:
            print(f"Error al insertar playlist: {e}")

    def insert_playlist_cancion(self, playlist_id, cancion_id):
        """Inserta una relación entre playlist y canción."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO playlist_canciones (playlist_id, cancion_id) VALUES (?, ?)
                ''', (playlist_id, cancion_id))
                conn.commit()
                print(f"Canción {cancion_id} añadida a la playlist {playlist_id}.")
        except sqlite3.Error as e:
            print(f"Error al insertar relación playlist-canción: {e}")

    def insert_fav(self, cancion_id):
        """Inserta una canción en la tabla de favoritos."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO favoritos (cancion_id) VALUES (?)
                ''', (cancion_id,))
                conn.commit()
                print(f"Canción {cancion_id} añadida a favoritos.")
        except sqlite3.Error as e:
            print(f"Error al insertar favorito: {e}")
