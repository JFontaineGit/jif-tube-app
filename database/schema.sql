-- Historial de Reproducción
CREATE TABLE IF NOT EXISTS historial_reproduccion (
    id INTEGER PRIMARY KEY,
    cancion_id TEXT NOT NULL,
    titulo TEXT NOT NULL,
    artista TEXT NOT NULL,
    fecha_reproduccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Playlists
CREATE TABLE IF NOT EXISTS playlists (
    id INTEGER PRIMARY KEY ,
    nombre TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relación Playlist-Canciones
CREATE TABLE IF NOT EXISTS playlist_canciones (
    id INTEGER PRIMARY KEY ,
    playlist_id INTEGER NOT NULL,
    cancion_id TEXT NOT NULL,
    FOREIGN KEY (playlist_id) REFERENCES playlists(id)
);

-- Favoritos
CREATE TABLE IF NOT EXISTS favoritos (
    id INTEGER PRIMARY KEY ,
    cancion_id TEXT NOT NULL
);