def agregar_usuario():
    print("=== Agregar usuario ===")
    try:
        with open("usuarios.txt", "a") as f:
            while True:
                uid = input("UID (8 caracteres hex, o ENTER para salir): ").strip().upper()
                if uid == "":
                    break
                if len(uid) != 8:
                    print("UID inválido. Debe tener 8 caracteres hexadecimales.")
                    continue
                nombre = input("Nombre del usuario: ").strip()
                f.write(f"{uid}:{nombre}\n")
                print(f"Guardado: {uid}:{nombre}")
    except Exception as e:
        print("Error al guardar:", e)

# LLAMAR explícitamente a la función
agregar_usuario()

# Leer luego de que se haya creado el archivo
with open("usuarios.txt", "r") as f:
    print("\nContenido actual del archivo:")
    print(f.read())