import network, socket, os

# === Wi-Fi Access Point ===
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP32-Usuarios', password='micropython123')
while not ap.active(): pass
print("Accede desde:", ap.ifconfig()[0])

# === Funciones auxiliares ===
def leer_usuarios():
    try:
        with open("usuarios.txt", "r") as f:
            return f.read()
    except:
        return "No hay usuarios registrados."

def guardar_usuario(uid, nombre):
    if len(uid) == 8 and nombre:
        with open("usuarios.txt", "a") as f:
            f.write(f"{uid}:{nombre}\n")
        return f"Guardado: {uid}:{nombre}"
    return "Datos inválidos."

def eliminar_usuario(uid):
    if len(uid) != 8: return "UID inválido."
    if "usuarios.txt" not in os.listdir(): return "Archivo no existe."
    with open("usuarios.txt", "r") as f:
        lineas = f.readlines()
    nueva = [l for l in lineas if not l.startswith(uid)]
    if len(nueva) == len(lineas): return "UID no encontrado."
    with open("usuarios.txt", "w") as f:
        f.writelines(nueva)
    return f"Eliminado: {uid}"

def pagina(mensaje=""):
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Gestión</title></head><body>
    <h1>ESP32 - Gestión de Usuarios</h1>
    <a href="/?a=ver"><button>Ver usuarios</button></a>
    <hr><h3>Agregar</h3>
    <form><input type="hidden" name="a" value="agregar">
    UID:<br><input name="uid"><br>Nombre:<br><input name="nombre"><br><input type="submit" value="Guardar"></form>
    <hr><h3>Eliminar</h3>
    <form><input type="hidden" name="a" value="eliminar">
    UID:<br><input name="uid"><br><input type="submit" value="Eliminar"></form>
    <hr><pre>{mensaje}</pre></body></html>"""

# === Servidor web ===
s = socket.socket()
s.bind(('0.0.0.0', 80))
s.listen(1)

while True:
    cl, addr = s.accept()
    req = cl.recv(1024).decode()
    print("Conexión:", addr)

    # Detectar acción
    msg = ""
    if "GET /?a=ver" in req:
        msg = leer_usuarios()
    elif "GET /?a=agregar" in req and "uid=" in req and "nombre=" in req:
        try:
            uid = req.split("uid=")[1].split("&")[0].split()[0].strip().upper()
            nombre = req.split("nombre=")[1].split()[0].replace("+", " ").strip()
            guardar_usuario(uid, nombre)
            cl.send("HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n")
            cl.close()
            continue
        except: msg = "Error al agregar."
    elif "GET /?a=eliminar" in req and "uid=" in req:
        try:
            uid = req.split("uid=")[1].split()[0].split("&")[0].strip().upper()
            eliminar_usuario(uid)
            cl.send("HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n")
            cl.close()
            continue
        except: msg = "Error al eliminar."

    # Página principal
    cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    cl.send(pagina(msg))
    cl.close()
