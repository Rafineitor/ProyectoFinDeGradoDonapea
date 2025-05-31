#Creo la función para agregar los usuarios al archivo usuarios.txt
def agregar_usuario():
    print("Agregar usuario")
    with open("usuarios.txt", "a") as f:
        while True:
            uid = input("Ingrese UID con 8 caracteres, o presione ENTER para salir): ").strip().upper()
            if uid == "":
                break
            if len(uid) != 8:
                print("Error, el UID debe tener 8 caracteres.")
                continue
            nombre = input("Nombre del usuario: ").strip()
            f.write(f"{uid}:{nombre}\n")
            print(f"Guardado: {uid}:{nombre}")
            

#Ejecuto la función
agregar_usuario()

#Leo la función después de que se creó
with open("usuarios.txt", "r") as f:
    print("\nContenido actual del archivo:")
    print(f.read())