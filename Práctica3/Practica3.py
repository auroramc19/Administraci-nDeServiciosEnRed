from trendCreate import crearTrend
from TrendUpdate import actualizarTrend
from threading import Thread
from getSNMPs import consultaSNMP
from datetime import datetime

import os.path

def agregarDispositivo():
    f = open('dispositivos.txt', 'a')
    host = input("Hostname/IP: ")
    comunidad = input("Comunidad: ")
    puerto = input("Puerto: ")
    rrd = 'practica3_D' + host.replace('.', '_')
    f.write(host + ", " + comunidad + ", " + puerto + ", " + rrd)
    f.write("\n")
    f.close();

    crearTrend(rrd)
    iniciarSondeo()


def eliminarDispositivo():
    mostrarArchivoDispositivos()

    index = int(input("Eliminar el dispositivo número: ")) - 1
    with open(r"dispositivos.txt", 'r+') as fp:
        lineas = fp.readlines()
        fp.seek(0)
        fp.truncate()
        for x, linea in enumerate(lineas):
            if x not in [index]:
                fp.write(linea)


def seleccionarDisp():
    mostrarArchivoDispositivos()
    index = int(input("Seleccione un dispositivo: ")) - 1

    with open("dispositivos.txt") as f:
        data = f.readlines()[index]
    data.split(", ")

    host = data.split(", ")[0]
    comunidad = data.split(", ")[1]
    puerto = data.split(", ")[2]

    #generarReporte(host, comunidad, puerto, index + 1)


def mostrarArchivoDispositivos():
    print("Dispositivos registrados:")
    i = 1
    with open("dispositivos.txt") as archivo:
        for linea in archivo:
            print(str(i) + ". " + linea)
            i = i + 1

def crearInventario(host, comunidad):

    date = datetime.now()
    MIB = '1.3.6.1.2.1'
    nameF = host.replace('.', '_')

    fname = f'Inventario/inventario_{nameF}.txt'
    if os.path.isfile(fname):
        return 0

    f = open(fname, 'a')

    # device
    dev = consultaSNMP(comunidad, host, MIB + '.1.5.0')
    f.write(f'Dispositivo: {dev}\n')

    #so
    so = str(consultaSNMP(comunidad, host, MIB + '.1.1.0'))
    soList = so.split()
    i = soList.index('Windows')
    if i < 0:
        i = so.index('Linux')
    system = soList[i:]
    sys = ''
    for s in system:
        sys = f'{sys} {s}'
    f.write(f'Versión Software: {sys}\n')

    #tiempo actividad
    timeAct = consultaSNMP(comunidad, host, MIB + '.25.1.1.0')
    f.write(f'Tiempo de actividad: {timeAct}\n')

    f.write(f'\nFecha y hora: {date.strftime("%d %b %Y %H:%M:%S")}\n')
    f.close()

def iniciarSondeo():
    with open("dispositivos.txt") as archivo:
        for linea in archivo:
            print(linea)
            host = linea.split(", ")[0]
            comunidad = linea.split(", ")[1]
            puerto = linea.split(", ")[2]
            rrd = linea.split(", ")[3].strip()
    crearInventario(host, comunidad)
    t1 = Thread(name="TrendUpdate", target=actualizarTrend, args=(comunidad, host, rrd,'deteccion_'+host.replace('.', '_')))
    t1.start()
    print("Inicio sondeo")



if __name__ == "__main__":
    opcion = 0

    fname = "dispositivos.txt"
    if os.path.isfile(fname):
        iniciarSondeo()

    while not (opcion == 4):
        print("\nAdquisición de información usando SNMP")
        print("1. Agregar dispositivo")
        print("2. Eliminar dispositivo")
        print("3. Generar reporte")
        print("4. Salir")

        opcion = int(input("\nElige una opción: "))

        if opcion == 1:
            print("\n")
            agregarDispositivo();
        elif opcion == 2:
            print("\n")
            eliminarDispositivo();
        elif opcion == 3:
            print("\n")
            seleccionarDisp()
        elif opcion == 4:
            break;
