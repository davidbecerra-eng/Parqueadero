"""
funciones.py
Funciones del negocio: registrar usuarios, vehiculos y
controlar la entrada y salida de vehiculos.
"""
from datetime import datetime
from database import conectar

FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"


# ---------------------------------------------------------------
# Usuarios y vehiculos
# ---------------------------------------------------------------
def registrar_usuario(nombre, documento, telefono):
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuario (nombre, documento, telefono) VALUES (?, ?, ?)",
            (nombre, documento, telefono))
        conexion.commit()
        return True, "Usuario registrado correctamente."
    except Exception:
        return False, "Ya existe un usuario con ese documento."
    finally:
        conexion.close()


def registrar_vehiculo(placa, tipo, documento_usuario):
    placa = placa.upper().strip()
    if tipo not in ("carro", "moto"):
        return False, "El tipo debe ser 'carro' o 'moto'."

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_usuario FROM usuario WHERE documento = ?",
                   (documento_usuario,))
    usuario = cursor.fetchone()
    if usuario is None:
        conexion.close()
        return False, "No existe un usuario con ese documento."

    try:
        cursor.execute(
            "INSERT INTO vehiculo (placa, tipo, id_usuario) VALUES (?, ?, ?)",
            (placa, tipo, usuario[0]))
        conexion.commit()
        return True, "Vehiculo registrado correctamente."
    except Exception:
        return False, "Esa placa ya esta registrada."
    finally:
        conexion.close()


# ---------------------------------------------------------------
# Entrada y salida
# ---------------------------------------------------------------
def registrar_entrada(placa):
    placa = placa.upper().strip()
    conexion = conectar()
    cursor = conexion.cursor()

    # 1. El vehiculo debe estar registrado (es por mensualidad)
    cursor.execute("SELECT id_vehiculo, tipo FROM vehiculo WHERE placa = ?",
                   (placa,))
    vehiculo = cursor.fetchone()
    if vehiculo is None:
        conexion.close()
        return False, "El vehiculo no esta registrado."
    id_vehiculo, tipo = vehiculo

    # 2. No puede entrar dos veces sin haber salido
    cursor.execute(
        "SELECT id_movimiento FROM movimiento "
        "WHERE id_vehiculo = ? AND fecha_salida IS NULL", (id_vehiculo,))
    if cursor.fetchone() is not None:
        conexion.close()
        return False, "Ese vehiculo ya se encuentra dentro del parqueadero."

    # 3. Buscar una celda libre del mismo tipo
    cursor.execute(
        "SELECT id_celda, numero FROM celda "
        "WHERE estado = 'libre' AND tipo = ? LIMIT 1", (tipo,))
    celda = cursor.fetchone()
    if celda is None:
        conexion.close()
        return False, "No hay celdas libres para este tipo de vehiculo."
    id_celda, numero_celda = celda

    # 4. Guardar la entrada y ocupar la celda
    ahora = datetime.now().strftime(FORMATO_FECHA)
    cursor.execute(
        "INSERT INTO movimiento (id_vehiculo, id_celda, fecha_entrada) "
        "VALUES (?, ?, ?)", (id_vehiculo, id_celda, ahora))
    cursor.execute("UPDATE celda SET estado = 'ocupada' WHERE id_celda = ?",
                   (id_celda,))
    conexion.commit()
    conexion.close()
    return True, f"Entrada registrada. Celda asignada: {numero_celda} ({ahora})"


def registrar_salida(placa):
    placa = placa.upper().strip()
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT m.id_movimiento, m.id_celda, m.fecha_entrada "
        "FROM movimiento m JOIN vehiculo v ON m.id_vehiculo = v.id_vehiculo "
        "WHERE v.placa = ? AND m.fecha_salida IS NULL", (placa,))
    movimiento = cursor.fetchone()
    if movimiento is None:
        conexion.close()
        return False, "Ese vehiculo no tiene una entrada activa."
    id_movimiento, id_celda, fecha_entrada = movimiento

    ahora = datetime.now()
    cursor.execute(
        "UPDATE movimiento SET fecha_salida = ? WHERE id_movimiento = ?",
        (ahora.strftime(FORMATO_FECHA), id_movimiento))
    cursor.execute("UPDATE celda SET estado = 'libre' WHERE id_celda = ?",
                   (id_celda,))
    conexion.commit()
    conexion.close()

    entrada = datetime.strptime(fecha_entrada, FORMATO_FECHA)
    minutos = int((ahora - entrada).total_seconds() // 60)
    return True, f"Salida registrada. Tiempo en el parqueadero: {minutos} minutos."


# ---------------------------------------------------------------
# Consultas
# ---------------------------------------------------------------
def vehiculos_dentro():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT v.placa, v.tipo, c.numero, m.fecha_entrada "
        "FROM movimiento m "
        "JOIN vehiculo v ON m.id_vehiculo = v.id_vehiculo "
        "JOIN celda c ON m.id_celda = c.id_celda "
        "WHERE m.fecha_salida IS NULL")
    filas = cursor.fetchall()
    conexion.close()
    return filas


def historial_movimientos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT v.placa, c.numero, m.fecha_entrada, m.fecha_salida "
        "FROM movimiento m "
        "JOIN vehiculo v ON m.id_vehiculo = v.id_vehiculo "
        "JOIN celda c ON m.id_celda = c.id_celda "
        "ORDER BY m.id_movimiento DESC")
    filas = cursor.fetchall()
    conexion.close()
    return filas


def celdas_libres():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT numero, tipo FROM celda WHERE estado = 'libre'")
    filas = cursor.fetchall()
    conexion.close()
    return filas
