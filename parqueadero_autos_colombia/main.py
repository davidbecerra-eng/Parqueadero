"""
main.py
Programa principal (menu por consola).
Parqueadero "Autos Colombia" - Iteracion 1: entrada y salida de vehiculos.
Iteracion 2: gestion de usuarios y gestion de celdas.
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
    print("8. Gestion de usuarios")
    print("9. Gestion de celdas")
    print("0. Salir")


def menu_usuarios():
    opcion = ""
    while opcion != "0":
        print()
        print("--- GESTION DE USUARIOS ---")
        print("1. Listar usuarios")
        print("2. Buscar usuario por documento")
        print("3. Actualizar usuario")
        print("4. Eliminar usuario")
        print("0. Volver")
        opcion = input("Elija una opcion: ").strip()

        if opcion == "1":
            filas = funciones.listar_usuarios()
            if len(filas) == 0:
                print("No hay usuarios registrados.")
            for documento, nombre, telefono, vehiculos in filas:
                print(f"{documento} | {nombre} | {telefono} | vehiculos: {vehiculos}")
        elif opcion == "2":
            usuario = funciones.buscar_usuario(input("Documento: "))
            if usuario is None:
                print("No existe un usuario con ese documento.")
            else:
                print(f"{usuario[0]} | {usuario[1]} | {usuario[2]}")
        elif opcion == "3":
            documento = input("Documento del usuario: ")
            nombre = input("Nuevo nombre: ")
            telefono = input("Nuevo telefono: ")
            print(funciones.actualizar_usuario(documento, nombre, telefono)[1])
        elif opcion == "4":
            print(funciones.eliminar_usuario(input("Documento del usuario: "))[1])
        elif opcion != "0":
            print("Opcion no valida.")


def menu_celdas():
    opcion = ""
    while opcion != "0":
        print()
        print("--- GESTION DE CELDAS ---")
        print("1. Listar todas las celdas")
        print("2. Crear celda")
        print("3. Cambiar estado (libre / mantenimiento)")
        print("4. Eliminar celda")
        print("0. Volver")
        opcion = input("Elija una opcion: ").strip()

        if opcion == "1":
            for numero, tipo, estado in funciones.listar_celdas():
                print(f"{numero} | {tipo} | {estado}")
        elif opcion == "2":
            numero = input("Numero de celda (ej. C-11): ")
            tipo = input("Tipo (carro/moto): ").lower().strip()
            print(funciones.crear_celda(numero, tipo)[1])
        elif opcion == "3":
            numero = input("Numero de celda: ")
            estado = input("Nuevo estado (libre/mantenimiento): ").lower().strip()
            print(funciones.cambiar_estado_celda(numero, estado)[1])
        elif opcion == "4":
            print(funciones.eliminar_celda(input("Numero de celda: "))[1])
        elif opcion != "0":
            print("Opcion no valida.")


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

        elif opcion == "8":
            menu_usuarios()

        elif opcion == "9":
            menu_celdas()

        elif opcion == "0":
            print("Hasta luego.")

        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    main()
