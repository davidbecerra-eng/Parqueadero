"""
main.py
Programa principal (menu por consola).
Parqueadero "Autos Colombia" - Iteracion 1: entrada y salida de vehiculos.
"""
from database import crear_tablas, cargar_celdas_iniciales
import funciones


def mostrar_menu():
    print()
    print("===== PARQUEADERO AUTOS COLOMBIA =====")
    print("1. Registrar usuario")
    print("2. Registrar vehiculo")
    print("3. Registrar entrada")
    print("4. Registrar salida")
    print("5. Ver vehiculos dentro del parqueadero")
    print("6. Ver celdas libres")
    print("7. Ver historial de movimientos")
    print("0. Salir")


def main():
    crear_tablas()
    cargar_celdas_iniciales()

    opcion = ""
    while opcion != "0":
        mostrar_menu()
        opcion = input("Elija una opcion: ").strip()

        if opcion == "1":
            nombre = input("Nombre: ")
            documento = input("Documento: ")
            telefono = input("Telefono: ")
            ok, mensaje = funciones.registrar_usuario(nombre, documento, telefono)
            print(mensaje)

        elif opcion == "2":
            placa = input("Placa: ")
            tipo = input("Tipo (carro/moto): ").lower().strip()
            documento = input("Documento del propietario: ")
            ok, mensaje = funciones.registrar_vehiculo(placa, tipo, documento)
            print(mensaje)

        elif opcion == "3":
            placa = input("Placa del vehiculo que entra: ")
            ok, mensaje = funciones.registrar_entrada(placa)
            print(mensaje)

        elif opcion == "4":
            placa = input("Placa del vehiculo que sale: ")
            ok, mensaje = funciones.registrar_salida(placa)
            print(mensaje)

        elif opcion == "5":
            filas = funciones.vehiculos_dentro()
            if len(filas) == 0:
                print("No hay vehiculos dentro.")
            for placa, tipo, celda, entrada in filas:
                print(f"{placa} | {tipo} | celda {celda} | entro: {entrada}")

        elif opcion == "6":
            for numero, tipo in funciones.celdas_libres():
                print(f"{numero} ({tipo})")

        elif opcion == "7":
            for placa, celda, entrada, salida in funciones.historial_movimientos():
                print(f"{placa} | {celda} | {entrada} -> {salida or 'sigue dentro'}")

        elif opcion == "0":
            print("Hasta luego.")

        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    main()
