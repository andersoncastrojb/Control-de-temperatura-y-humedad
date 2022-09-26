# Write your code here :-)
import json
from machine import Pin
from time import sleep
import network

# Libreria Mqtt
from umqttsimple import MQTTClient
import dht

# Connect to internet
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        # wlan.connect('CLARO_WIFI5E0', 'CLAROI5E0')
        wlan.connect("Wi-Fi Unimagdalena", None)
        while not wlan.isconnected():
            pass
    print("network config:", wlan.ifconfig())
    # Para desconectar del wifi
    # wlan.disconnect()


# Declarar pin para datos de sensor DHT11
sensor = dht.DHT11(Pin(18, Pin.IN, Pin.PULL_UP))

# Función para leer los datos del sensor DHT11 y retornar Temperatura y Humedad
def read_sensor():
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        if (isinstance(temp, float) and isinstance(hum, float)) or (
            isinstance(temp, int) and isinstance(hum, int)
        ):
            temp = b"{0:3.1f},".format(temp)
            hum = b"{0:3.1f},".format(hum)

            # uncomment for Fahrenheit
            # temp = temp * (9/5) + 32.0
            return temp, hum
        else:
            return "Invalid sensor readings."
    except:
        return "Error sensor readings."


# Declarar pin de control para el humificador ON-OFF (se activa con cero)
humificador = Pin(2, Pin.OUT)
humificador.on()
# Declarar pin de control para el ventilador ON-OFF (se activa con cero)
ventilador = Pin(5, Pin.OUT, Pin.PULL_DOWN)
ventilador.on()
# Declarar pin de control para el ventilador del humificador ON-OFF (se activa con cero)
ventiHum = Pin(4, Pin.OUT)
ventiHum.on()

# Connect to internet
do_connect()

# Mqtt process
########################################
SERVER = "34.196.108.0"
client = MQTTClient("be-caribe-topic", SERVER)
topic = "be-caribe-topic"
try:
    client.connect()
    print("conexión mqtt exitosa!\n")
except OSError as e:
    print(e)
########################################

sleep(2)
Humedad:
95.0
on Ventiladores
on Ventilador y Humificador
Temperatura:
27.0
Humedad:
95.0
on Ventiladores
on Ventilador y Humificador
Temperatura:
27.0
Humedad:
95.0
on Ventiladores
cont = 0
while True:
    try:
        # print("Enviados!!")
        datos = read_sensor()
        try:
            dtemp = str(datos[0])
            dhum = str(datos[1])
            dtemp = float((dtemp[2:6]))
            dhum = float((dhum[2:6]))
        except:
            dtemp = 35
            dhum = 40


        # data vector
        d = {
            "device_name": "Be_Caribe_01",
            "rt_temperature": dtemp,
            "rt_humidity": dhum,
        }
        datos = json.dumps(d)

        # Almacenamiento y envio de datos
        client.publish(topic, str(datos))
        """
       for i in datos:
           client.publish(topic, str(i))
       """

        # Imprime la temperatura en °C
        print("Temperatura: ")
        print(dtemp)
        # Imprime la humedad
        print("Humedad: ")
        print(dhum)

        # Si la temperatura es igual o superior a 30 activa los ventiladores
        if dtemp >= 25.0:
            print("on Ventiladores")
            ventilador.on()
        else:
            print("off Ventiladores")
            ventilador.off()

        # Si la humedad es igual o inferior a 95 activa el humificador y su ventilador
        if dhum >= 91:
            print("on Ventilador y Humificador")
            humificador.on()
            ventiHum.on()
        else:
            print("off Ventilador y Humificador")
            humificador.off()
            ventiHum.off()

    except OSError as e:
        print(e)

    # Secs
    sleep(7)
