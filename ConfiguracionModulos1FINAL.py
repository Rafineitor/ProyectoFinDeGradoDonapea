from machine import Pin, PWM, I2C
import time
import mfrc522
from i2c_lcd import I2cLcd

#Pines de placa RFID, servo y leds
SCK = 18
MOSI = 23
MISO = 19
RST = 27
CS = 5
SERVO_PIN = 4
LED_VERDE = 12
LED_ROJO = 14

#Inicialización de módulos
rdr = mfrc522.MFRC522(sck=SCK, mosi=MOSI, miso=MISO, rst=RST, cs=CS)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
lcd = I2cLcd(i2c, 0x27, 2, 16)
servo = PWM(Pin(SERVO_PIN), freq=50)
led_verde = Pin(LED_VERDE, Pin.OUT)
led_rojo = Pin(LED_ROJO, Pin.OUT)


#Mover servo
def mover_servo(angulo):
    duty = int((angulo / 180) * 75 + 40)
    servo.duty(duty)
 
#Carga usuarios desde archivo usuarios.txt
def cargar_usuarios():
    
    usuarios = {}
    with open("usuarios.txt", "r") as f:
        for linea in f:
            linea = linea.strip()
            if ":" in linea:
                uid_str, nombre = linea.split(":")
                usuarios[uid_str.upper()] = nombre
    return usuarios

def scroll_infinito(texto, fila=0, pasos=1, pausa=0.2):
    texto_scroll = texto + "   "
    for _ in range(pasos * len(texto_scroll)):
        lcd.move_to(0, fila)
        lcd.putstr(texto_scroll[:16])
        texto_scroll = texto_scroll[1:] + texto_scroll[0]
        time.sleep(pausa)
        (stat, _) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            return True
    return False


usuarios = cargar_usuarios()

def mostrar_mensaje(texto, fila=0):
    lcd.clear()
    lcd.move_to(0, fila)
    lcd.putstr(texto)

# Inicio
mostrar_mensaje("Escanea tu tarjeta")
mover_servo(0)

# Bucle principal
usuarios = cargar_usuarios()
mover_servo(0)

while True:
    if scroll_infinito("Escanea tu tarjeta", fila=0, pasos=1):
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            uid_bytes = raw_uid[:4]
            uid_str = "".join("{:02X}".format(b) for b in uid_bytes)
            print("UID detectado:", uid_str)

            if uid_str in usuarios:
                nombre = usuarios[uid_str]
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Bienvenido/a,")
                lcd.move_to(0, 1)
                lcd.putstr(nombre[:16])
                led_verde.on()
                mover_servo(120)
                time.sleep(3)
                mover_servo(0)
                lcd.move_to(0, 1)
                lcd.putstr(" " * 16)
                led_verde.off()
            else:
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Acceso denegado")
                led_rojo.on()
                time.sleep(2)
                led_rojo.off()
