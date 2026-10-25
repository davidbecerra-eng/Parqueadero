# Parqueadero "Autos Colombia" - Iteración 1

Sistema de información para la gestión de **entrada y salida de vehículos**
de un parqueadero por mensualidad.

## Qué hace esta versión

- Registrar usuarios (propietarios).
- Registrar vehículos asociados a un usuario.
- Registrar la **entrada** de un vehículo (asigna una celda libre del mismo tipo).
- Registrar la **salida** de un vehículo (libera la celda y calcula el tiempo).
- Consultar vehículos dentro, celdas libres e historial.

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

## Prueba rápida

1. Opción 1: registrar usuario (ej. Juan Pérez, documento 123).
2. Opción 2: registrar vehículo (placa ABC123, carro, documento 123).
3. Opción 3: entrada de ABC123.
4. Opción 5: ver que aparece dentro.
5. Opción 4: salida de ABC123.

## Pendiente para próximas iteraciones

Gestión de pagos, novedades y administración completa de celdas.
