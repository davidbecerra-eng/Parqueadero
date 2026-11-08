# Parqueadero "Autos Colombia" - Iteraciones 1 y 2

Sistema de información para la gestión de un parqueadero por mensualidad.

- **Iteración 1:** entrada y salida de vehículos.
- **Iteración 2:** gestión de usuarios y gestión de celdas.

## Qué hace esta versión

- Registrar usuarios (propietarios).
- Registrar vehículos asociados a un usuario.
- Registrar la **entrada** de un vehículo (asigna una celda libre del mismo tipo).
- Registrar la **salida** de un vehículo (libera la celda y calcula el tiempo).
- Consultar vehículos dentro, celdas libres e historial.

### Novedades de la Iteración 2

**Gestión de usuarios** (opción 8 del menú): listar, buscar por documento,
actualizar nombre/teléfono y eliminar (solo si el usuario no tiene vehículos).

**Gestión de celdas** (opción 9 del menú): listar todas, crear, cambiar el estado
a *libre* o *mantenimiento* (una celda en mantenimiento no se asigna) y eliminar
(solo si no está ocupada ni tiene historial).

## Tecnologías

- Python 3
- SQLite (viene incluido con Python, no hay que instalar nada)

## Cómo ejecutarlo

```bash
python main.py
```

La base de datos `parqueadero.db` se crea sola la primera vez, junto con
15 celdas de prueba (10 de carro y 5 de moto).

## Estructura

| Archivo | Descripción |
|---|---|
| `main.py` | Menú por consola |
| `funciones.py` | Lógica: usuarios, vehículos, entradas y salidas |
| `database.py` | Conexión y creación de tablas |
| `pruebas_iteracion2.py` | Ejecuta el plan de pruebas de la Iteración 2 (23 casos) |

## Prueba rápida

1. Opción 1: registrar usuario (ej. Juan Pérez, documento 123).
2. Opción 2: registrar vehículo (placa ABC123, carro, documento 123).
3. Opción 3: entrada de ABC123.
4. Opción 5: ver que aparece dentro.
5. Opción 4: salida de ABC123.

## Pruebas

```bash
python pruebas_iteracion2.py
```

Usa una base de datos temporal, así que no modifica `parqueadero.db`.

## Pendiente para próximas iteraciones

Gestión de pagos y registro de novedades.
