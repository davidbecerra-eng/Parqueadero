"""
database.py
Conexion a la base de datos SQLite y creacion de las tablas.
Parqueadero "Autos Colombia" - Iteracion 1
"""
import sqlite3

NOMBRE_BD = "parqueadero.db"


def conectar():
    """Abre la conexion con la base de datos."""
    conexion = sqlite3.connect(NOMBRE_BD)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    """Crea las tablas si todavia no existen."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre     TEXT NOT NULL,
            documento  TEXT NOT NULL UNIQUE,
            telefono   TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehiculo (
            id_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
            placa       TEXT NOT NULL UNIQUE,
            tipo        TEXT NOT NULL,
            id_usuario  INTEGER NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS celda (
            id_celda INTEGER PRIMARY KEY AUTOINCREMENT,
            numero   TEXT NOT NULL UNIQUE,
            tipo     TEXT NOT NULL,
            estado   TEXT NOT NULL DEFAULT 'libre'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimiento (
            id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_vehiculo   INTEGER NOT NULL,
            id_celda      INTEGER NOT NULL,
            fecha_entrada TEXT NOT NULL,
            fecha_salida  TEXT,
            FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id_vehiculo),
            FOREIGN KEY (id_celda)    REFERENCES celda(id_celda)
        )
    """)

    conexion.commit()
    conexion.close()


def cargar_celdas_iniciales():
    """Si no hay celdas, crea 10 de carro y 5 de moto para poder probar."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM celda")
    cantidad = cursor.fetchone()[0]

    if cantidad == 0:
        for i in range(1, 11):
            cursor.execute("INSERT INTO celda (numero, tipo) VALUES (?, ?)",
                           (f"C-{i:02d}", "carro"))
        for i in range(1, 6):
            cursor.execute("INSERT INTO celda (numero, tipo) VALUES (?, ?)",
                           (f"M-{i:02d}", "moto"))
        conexion.commit()

    conexion.close()
