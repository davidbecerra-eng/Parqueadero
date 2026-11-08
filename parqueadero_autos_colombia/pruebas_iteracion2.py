"""
pruebas_iteracion2.py
Ejecuta el plan de pruebas de la Iteracion 2 (usuarios y celdas) sobre una
base de datos temporal, sin tocar parqueadero.db.

Uso:  python pruebas_iteracion2.py
"""
import json
import os
import tempfile

import database
import funciones as f

# Base de datos temporal para no afectar los datos reales
database.NOMBRE_BD = os.path.join(tempfile.mkdtemp(), "prueba.db")
database.crear_tablas()
database.cargar_celdas_iniciales()

resultados = []


def caso(id_, modulo, descripcion, entrada, esperado, funcion, verifica):
    """Ejecuta una prueba y guarda el resultado obtenido."""
    obtenido = funcion()
    texto = obtenido[1] if isinstance(obtenido, tuple) else str(obtenido)
    estado = "Exitosa" if verifica(obtenido) else "Fallida"
    resultados.append({"id": id_, "modulo": modulo, "descripcion": descripcion,
                       "entrada": entrada, "esperado": esperado,
                       "obtenido": texto, "estado": estado})


ok = lambda r: r[0] is True
no = lambda r: r[0] is False

# ---------------- Usuarios ----------------
caso("PU-01", "Usuarios", "Registrar usuario nuevo",
     "Juan Perez, 123, 3001112233", "Usuario registrado",
     lambda: f.registrar_usuario("Juan Perez", "123", "3001112233"), ok)
caso("PU-02", "Usuarios", "Registrar usuario con documento repetido",
     "Otro, 123, 300", "Rechaza: documento ya existe",
     lambda: f.registrar_usuario("Otro", "123", "300"), no)
f.registrar_usuario("Ana Gomez", "456", "3104445566")
caso("PU-03", "Usuarios", "Listar usuarios",
     "(sin datos)", "Muestra 2 usuarios",
     lambda: (True, f"{len(f.listar_usuarios())} usuarios"),
     lambda r: r[1] == "2 usuarios")
caso("PU-04", "Usuarios", "Buscar usuario existente",
     "Documento 123", "Devuelve Juan Perez",
     lambda: (True, str(f.buscar_usuario("123"))),
     lambda r: "Juan Perez" in r[1])
caso("PU-05", "Usuarios", "Buscar usuario inexistente",
     "Documento 999", "No devuelve datos",
     lambda: (True, str(f.buscar_usuario("999"))),
     lambda r: r[1] == "None")
caso("PU-06", "Usuarios", "Actualizar nombre y telefono",
     "123, Juan P. Rojas, 3200000000", "Usuario actualizado",
     lambda: f.actualizar_usuario("123", "Juan P. Rojas", "3200000000"), ok)
caso("PU-07", "Usuarios", "Actualizar usuario inexistente",
     "999, X, 1", "Rechaza: no existe",
     lambda: f.actualizar_usuario("999", "X", "1"), no)
caso("PU-08", "Usuarios", "Actualizar con nombre vacio",
     "123, (vacio), 1", "Rechaza: nombre vacio",
     lambda: f.actualizar_usuario("123", "  ", "1"), no)
f.registrar_vehiculo("ABC123", "carro", "123")
caso("PU-09", "Usuarios", "Eliminar usuario con vehiculos",
     "Documento 123", "Rechaza: tiene vehiculos",
     lambda: f.eliminar_usuario("123"), no)
caso("PU-10", "Usuarios", "Eliminar usuario sin vehiculos",
     "Documento 456", "Usuario eliminado",
     lambda: f.eliminar_usuario("456"), ok)
caso("PU-11", "Usuarios", "Eliminar usuario inexistente",
     "Documento 999", "Rechaza: no existe",
     lambda: f.eliminar_usuario("999"), no)

# ---------------- Celdas ----------------
caso("PC-01", "Celdas", "Crear celda nueva",
     "C-11, carro", "Celda creada",
     lambda: f.crear_celda("C-11", "carro"), ok)
caso("PC-02", "Celdas", "Crear celda con numero repetido",
     "C-11, carro", "Rechaza: numero ya existe",
     lambda: f.crear_celda("C-11", "carro"), no)
caso("PC-03", "Celdas", "Crear celda con tipo invalido",
     "X-01, camion", "Rechaza: tipo invalido",
     lambda: f.crear_celda("X-01", "camion"), no)
caso("PC-04", "Celdas", "Listar todas las celdas",
     "(sin datos)", "Muestra 16 celdas (15 iniciales + C-11)",
     lambda: (True, f"{len(f.listar_celdas())} celdas"),
     lambda r: r[1] == "16 celdas")
caso("PC-05", "Celdas", "Poner celda en mantenimiento",
     "C-11, mantenimiento", "Estado cambia a mantenimiento",
     lambda: f.cambiar_estado_celda("C-11", "mantenimiento"), ok)
def _sin_celdas_carro_libres():
    """Pone TODAS las celdas de carro en mantenimiento e intenta una entrada."""
    for n in ["C-%02d" % i for i in range(1, 11)] + ["C-11"]:
        f.cambiar_estado_celda(n, "mantenimiento")
    return f.registrar_entrada("ABC123")


caso("PC-06", "Celdas", "Celdas en mantenimiento no se asignan",
     "Todas las celdas de carro en mantenimiento; entrada de ABC123",
     "Rechaza: no hay celdas libres para carro",
     _sin_celdas_carro_libres, no)
for _n in ["C-%02d" % _i for _i in range(1, 11)]:
    f.cambiar_estado_celda(_n, "libre")
f.registrar_entrada("ABC123")   # ocupa C-01 para las pruebas siguientes
caso("PC-07", "Celdas", "Cambiar estado de celda ocupada",
     "C-01, mantenimiento", "Rechaza: celda ocupada",
     lambda: f.cambiar_estado_celda("C-01", "mantenimiento"), no)
caso("PC-08", "Celdas", "Estado invalido",
     "C-02, roto", "Rechaza: estado invalido",
     lambda: f.cambiar_estado_celda("C-02", "roto"), no)
caso("PC-09", "Celdas", "Cambiar estado de celda inexistente",
     "Z-99, libre", "Rechaza: no existe",
     lambda: f.cambiar_estado_celda("Z-99", "libre"), no)
caso("PC-10", "Celdas", "Eliminar celda ocupada",
     "C-01", "Rechaza: celda ocupada",
     lambda: f.eliminar_celda("C-01"), no)
caso("PC-11", "Celdas", "Eliminar celda con historial",
     "C-01 tras la salida de ABC123", "Rechaza: tiene movimientos",
     lambda: (f.registrar_salida("ABC123"), f.eliminar_celda("C-01"))[1], no)
caso("PC-12", "Celdas", "Eliminar celda libre sin historial",
     "C-11 (se vuelve a 'libre' antes)", "Celda eliminada",
     lambda: (f.cambiar_estado_celda("C-11", "libre"), f.eliminar_celda("C-11"))[1], ok)

if __name__ == "__main__":
    for r in resultados:
        print(f"{r['id']} [{r['estado']}] {r['descripcion']} -> {r['obtenido']}")
    fallidas = [r for r in resultados if r["estado"] != "Exitosa"]
    print(f"\n{len(resultados) - len(fallidas)}/{len(resultados)} pruebas exitosas")
    with open("resultados_pruebas.json", "w", encoding="utf-8") as archivo:
        json.dump(resultados, archivo, ensure_ascii=False, indent=2)
