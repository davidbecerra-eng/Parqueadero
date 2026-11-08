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


# ===============================================================
# ITERACION 2 - Gestion de usuarios
# ===============================================================
def listar_usuarios():
    """Devuelve (documento, nombre, telefono, cantidad_vehiculos)."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT u.documento, u.nombre, u.telefono, COUNT(v.id_vehiculo) "
        "FROM usuario u LEFT JOIN vehiculo v ON v.id_usuario = u.id_usuario "
        "GROUP BY u.id_usuario ORDER BY u.nombre")
    filas = cursor.fetchall()
    conexion.close()
    return filas


def buscar_usuario(documento):
    """Devuelve (documento, nombre, telefono) o None si no existe."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT documento, nombre, telefono FROM usuario "
                   "WHERE documento = ?", (documento,))
    fila = cursor.fetchone()
    conexion.close()
    return fila


def actualizar_usuario(documento, nombre, telefono):
    """Actualiza nombre y telefono de un usuario (el documento no cambia)."""
    if not nombre.strip():
        return False, "El nombre no puede estar vacio."
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("UPDATE usuario SET nombre = ?, telefono = ? "
                   "WHERE documento = ?", (nombre.strip(), telefono, documento))
    conexion.commit()
    modificado = cursor.rowcount
    conexion.close()
    if modificado == 0:
        return False, "No existe un usuario con ese documento."
    return True, "Usuario actualizado correctamente."


def eliminar_usuario(documento):
    """Elimina un usuario solo si no tiene vehiculos asociados."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_usuario FROM usuario WHERE documento = ?",
                   (documento,))
    usuario = cursor.fetchone()
    if usuario is None:
        conexion.close()
        return False, "No existe un usuario con ese documento."

    cursor.execute("SELECT COUNT(*) FROM vehiculo WHERE id_usuario = ?",
                   (usuario[0],))
    if cursor.fetchone()[0] > 0:
        conexion.close()
        return False, "No se puede eliminar: el usuario tiene vehiculos registrados."

    cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (usuario[0],))
    conexion.commit()
    conexion.close()
    return True, "Usuario eliminado correctamente."


# ===============================================================
# ITERACION 2 - Gestion de celdas
# ===============================================================
ESTADOS_CELDA = ("libre", "ocupada", "mantenimiento")


def crear_celda(numero, tipo):
    numero = numero.upper().strip()
    if not numero:
        return False, "El numero de celda no puede estar vacio."
    if tipo not in ("carro", "moto"):
        return False, "El tipo debe ser 'carro' o 'moto'."
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO celda (numero, tipo) VALUES (?, ?)",
                       (numero, tipo))
        conexion.commit()
        return True, "Celda creada correctamente."
    except Exception:
        return False, "Ya existe una celda con ese numero."
    finally:
        conexion.close()


def listar_celdas():
    """Devuelve (numero, tipo, estado) de todas las celdas."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT numero, tipo, estado FROM celda ORDER BY numero")
    filas = cursor.fetchall()
    conexion.close()
    return filas


def cambiar_estado_celda(numero, estado):
    """Pone una celda en 'libre' o 'mantenimiento'. Una celda ocupada no se toca."""
    numero = numero.upper().strip()
    if estado not in ("libre", "mantenimiento"):
        return False, "El estado debe ser 'libre' o 'mantenimiento'."
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT estado FROM celda WHERE numero = ?", (numero,))
    celda = cursor.fetchone()
    if celda is None:
        conexion.close()
        return False, "No existe una celda con ese numero."
    if celda[0] == "ocupada":
        conexion.close()
        return False, "No se puede cambiar el estado: la celda esta ocupada."
    cursor.execute("UPDATE celda SET estado = ? WHERE numero = ?",
                   (estado, numero))
    conexion.commit()
    conexion.close()
    return True, f"La celda {numero} ahora esta en estado '{estado}'."


def eliminar_celda(numero):
    """Elimina una celda solo si no esta ocupada y nunca ha tenido movimientos."""
    numero = numero.upper().strip()
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_celda, estado FROM celda WHERE numero = ?",
                   (numero,))
    celda = cursor.fetchone()
    if celda is None:
        conexion.close()
        return False, "No existe una celda con ese numero."
    if celda[1] == "ocupada":
        conexion.close()
        return False, "No se puede eliminar: la celda esta ocupada."
    cursor.execute("SELECT COUNT(*) FROM movimiento WHERE id_celda = ?",
                   (celda[0],))
    if cursor.fetchone()[0] > 0:
        conexion.close()
        return False, "No se puede eliminar: la celda tiene movimientos en el historial."
    cursor.execute("DELETE FROM celda WHERE id_celda = ?", (celda[0],))
    conexion.commit()
    conexion.close()
    return True, "Celda eliminada correctamente."
