from machine import Pin, PWM, I2C
import time
import mfrc522
from i2c_lcd import I2cLcd

# Pines
SCK = 18
MOSI = 23
MISO = 19
RST = 27
SDA = 5
SERVO_PIN = 4

# Inicialización de módulos
rdr = mfrc522.MFRC522(sck=SCK, mosi=MOSI, miso=MISO, rst=RST, sda=SDA)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
lcd = I2cLcd(i2c, 0x27, 2, 16)
servo = PWM(Pin(SERVO_PIN), freq=50)

# Mueve el servo
def mover_servo(angulo):
    duty = int((angulo / 180) * 75 + 40)
    servo.duty(duty)
 
# Carga usuarios desde archivo
def cargar_usuarios():
    usuarios = {}
    try:
        with open("usuarios.txt", "r") as f:
            for linea in f:
                linea = linea.strip()
                if ":" in linea:
                    uid_str, nombre = linea.split(":")
                    usuarios[uid_str.upper()] = nombre
    except Exception as e:
        print("Error al leer usuarios.txt:", e)
    return usuarios

usuarios = cargar_usuarios()

def mostrar_mensaje(texto, fila=0):
    lcd.clear()
    lcd.move_to(0, fila)
    lcd.putstr(texto)

# Inicio
mostrar_mensaje("Escanea tu tarjeta")
mover_servo(0)

# Bucle principal
while True:
    uid = None
    (stat, _) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            uid_bytes = raw_uid[:4]
            uid_str = "".join("{:02X}".format(b) for b in uid_bytes)
            print("UID detectado:", uid_str)

            if uid_str in usuarios:
                nombre = usuarios[uid_str]
                mostrar_mensaje(f"Bienvenido/a,")
                lcd.move_to(0, 1)
                lcd.putstr(nombre[:16])
                mover_servo(120)
                time.sleep(3)
                mover_servo(0)
            else:
                mostrar_mensaje("Acceso denegado")
                time.sleep(2)

            mostrar_mensaje("Escanea tu tarjeta")

    time.sleep(0.2)