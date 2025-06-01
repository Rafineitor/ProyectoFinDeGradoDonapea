import os


#Función par ver usuarios registrados
def ver_usuarios():
    
    print("\nUsuarios registrados")
    if "usuarios.txt" in os.listdir():
        with open("usuarios.txt", "r") as f:
            lineas = f.readlines()
            if not lineas:
                print("No hay usuarios registrados.")
            else:
                for idx, linea in enumerate(lineas):
                    print(f"{idx+1}. {linea.strip()}")


#Función para agregar un usuario
def agregar_usuario():
    
    print("\nAgregar usuario")
    with open("usuarios.txt", "a") as f:
        while True:
            uid = input("Ingrese UID con 8 caracteres o presione ENTER para salir): ").strip().upper()
            if uid == "":
                break
            if len(uid) != 8:
                print("Error, el UID debe tener 8 caracteres.")
                continue
            nombre = input("Nombre del usuario:")
            f.write(f"{uid}:{nombre}\n")
            print(f"Guardado: {uid}:{nombre}")


#Función para eliminar un usuario.
def eliminar_usuario():
    
    print("\nEliminar usuario por UID")
    with open("usuarios.txt", "r") as f: #Abre archivo para leerlo.
        lineas = f.readlines() #Crea la variable lineas con las lineas en el archivo.

    if not lineas:
        print("No hay usuarios registrados.") #Si no hay lineas contenidas imprime.
        return

    print("Usuarios actuales:")
    for linea in lineas:
        print("-", linea.strip())

    entrada = input("\nEscribe el UID a eliminar o presione ENTER para cancelar): ").strip().upper() #Se ingresa UID a eliminar.
    if entrada == "":
        print("Cancelado.") #Si no perciben entrada imprime.
        return

    nueva_lista = []
    eliminado = False
    for linea in lineas: #Va recorriendo las lineas.
        if not linea.startswith(entrada): #certifica si no comienza con el input "entrada".
            nueva_lista.append(linea)
        else:
            print("Eliminado: {linea.strip()}")
            eliminado = True

    if not eliminado:
        print("UID no encontrado.")
        return

    with open("usuarios.txt", "w") as f: #Abre el archivo y agrega la nueva lista en él.
        f.writelines(nueva_lista)


#Menú principal
def menu_usuarios():
    
    if "usuarios.txt" not in os.listdir():
        with open("usuarios.txt", "w") as f:
            pass

    while True:
        print("\nMENÚ DE USUARIOS")#Imprime todo el menú
        print("1. Ver usuarios")
        print("2. Agregar usuario")
        print("3. Eliminar usuario")
        print("0. Salir")
        
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            ver_usuarios()
        elif opcion == "2":
            agregar_usuario()
        elif opcion == "3":
            eliminar_usuario()
        elif opcion == "0":
            print("Saliendo del menú.")
            break
        else:
            print("Opción inválida.")

# Ejecuta menú
menu_usuarios()