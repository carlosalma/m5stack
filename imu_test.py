"""
Autor: CAM
Fecha: 03/11/2024

Ejemplos de uso de la unidad IMU.

NOTA
El código solo se ha verificado sobre M5Stack Core2 ESP32

REFERENCIA 
Basado en los ejemplos escritos en c por Luís Llamas
https://www.luisllamas.es/arduino-orientacion-imu-mpu-6050/
"""

import os, sys, io
import M5
import math
import time
from M5 import *

title0 = None
label1 = None
label2 = None
label3 = None

def aceleracion_raw():
    """Aceleración, datos directos de la MPU"""
    ax = Imu.getAccel()[0]
    ay = Imu.getAccel()[1]
    az = Imu.getAccel()[2]
    return ax, ay, az

def vel_angular_raw():
    """Velocidad angular, datos director de la MPU"""
    vx = Imu.getGyro()[0]
    vy = Imu.getGyro()[1]
    vz = Imu.getGyro()[2]
    return vx, vy, vz

def aceleracion_en_si():
    """Aceleración en Sistema Internacional (G)"""
    escalado = 2.0 * 9.81 / 32768.0
    ax_si = aceleracion_raw()[0] * escalado
    ay_si = aceleracion_raw()[1] * escalado
    az_si = aceleracion_raw()[2] * escalado
    return ax_si, ay_si, az_si

def vel_angular_en_si():
    """Velocidad angular en Sistema Internacional (º/s)"""
    escalado = 250.0 / 32768.0
    vx_si = vel_angular_raw()[0] * escalado
    vy_si = vel_angular_raw()[1] * escalado
    vz_si = vel_angular_raw()[2] * escalado
    return vx_si, vy_si, vz_si    

def inclinacion_en_grados(redondeo):
    """Inclinación en grados"""
    ac_ang_x = math.atan(aceleracion_raw()[0] / math.sqrt(math.pow(aceleracion_raw()[1], 2) + math.pow(aceleracion_raw()[2], 2))) * (180.0 / 3.14);
    ac_ang_y = math.atan(aceleracion_raw()[1] / math.sqrt(math.pow(aceleracion_raw()[0], 2) + math.pow(aceleracion_raw()[2], 2))) * (180.0 / 3.14);
    return round(ac_ang_x, redondeo), round(ac_ang_y, redondeo)

def ui():
    """Interface de Usuario"""
    global title0, label1, label2, label3
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("USO: IMU (ver: 0.1)", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    
    label1 = Widgets.Label("", 1, 40, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu12)
    label2 = Widgets.Label("", 1, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu12)
    label3 = Widgets.Label("", 1, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu12)

def datos_acelerometro(lbl1, lbl2, lbl3):
    """Muestra los datos del acelerómetro"""
    global title0, label1, label2, label3    
    label1.setText(lbl1 + str(aceleracion_en_si()[0]))
    label2.setText(lbl2 + str(aceleracion_en_si()[1]))
    label3.setText(lbl3 + str(aceleracion_en_si()[2]))

def datos_vel_angular(lbl1, lbl2, lbl3):
    """Muestra los datos del acelerómetro"""
    global title0, label1, label2, label3    
    label1.setText(lbl1 + str(vel_angular_en_si()[0]))
    label2.setText(lbl2 + str(vel_angular_en_si()[1]))
    label3.setText(lbl3 + str(vel_angular_en_si()[2]))

def datos_inclinacion(lbl1, lbl2, redondeo):
    """Muestra los datos de inclinación en grados"""
    global title0, label1, label2
    label1.setText(lbl1 + str(inclinacion_en_grados(redondeo)[0]))
    label2.setText(lbl2 + str(inclinacion_en_grados(redondeo)[1]))
   
def datos_selector(selector):
    """ """
    if selector == 1:
        datos_acelerometro("ACEL X: ", "ACEL Y: ", "ACEL Z: ")
    elif selector == 2:    
        datos_vel_angular("VEL ANG X: ", "VEL ANG Y: ", "VEL ANG Z: ")
    elif selector == 3:
        datos_inclinacion("ANGULO X: ", "ANGULO Y: ", 2)
        
def setup():
    """ """
    M5.begin()
    ui()
    
def loop():
    """ """
    M5.update()
    datos_selector(3)
    time.sleep(0.2)
    
if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

