from datetime import datetime
import os.path
import getpass
import Servicios


def agregarDispositivo():
    f = open('dispositivos.txt', 'a')
    host = input("Hostname/IP: ")
    #comunidad = input("Comunidad: ")
    #puerto = input("Puerto: ")
    #rrd = 'practica4_D' + host.replace('.', '_')
    f.write(host + ", ")
    f.write("\n")
    f.close()

    #crearTrend(rrd)
    #iniciarSondeo()

def mostrarArchivoDispositivos():
    print("Dispositivos registrados:")
    i = 1
    with open("dispositivos.txt") as archivo:
        for linea in archivo:
            print(str(i) + ". " + linea)
            i = i + 1

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

def menuAdminConfig():
    opcion = 0
    while not (opcion == 4):
        mostrarArchivoDispositivos()
        index = int(input("Seleccione un dispositivo: ")) - 1

        with open("dispositivos.txt") as f:
            data = f.readlines()[index]
        data.split(", ")

        host = data.split(", ")[0]
        print(host)
        print("\nAdministración de configuración")
        print("1. Generar el archivo de configuracion")
        print("2. Extraer el archivo de configuración")
        print("3. Mandar archivo de configuración al router")
        print("4. Regresar")

        opcion = int(input("\nElige una opción: "))

        print("\n")
        if opcion == 1:
            user = input("Usuario: ")
            pwd = getpass.getpass()
            Servicios.generarArchivoConfig(host,user,pwd)
        elif opcion == 2:
            user = input("Usuario: ")
            pwd = getpass.getpass()
            nomArchivo = input("Nombre del archivo (default 'startup-config'): ")
            Servicios.extraerArchivoConfig(host, user, pwd, nomArchivo)
        elif opcion == 3:
            user = input("Usuario: ")
            pwd = getpass.getpass()
            nomArchivo = input("Nombre del archivo (default 'startup-config'): ")
            Servicios.enviarArchivoConfig(host, user, pwd, nomArchivo)
        elif opcion == 4:
            break

if __name__ == "__main__":
    opcion = 0

    #fname = "dispositivos.txt"
    #if os.path.isfile(fname):
    #    iniciarSondeo()

    while not (opcion == 4):
        print("\nPráctica 4 - Administración de configuración")
        print("1. Agregar dispositivo")
        print("2. Eliminar dispositivo")
        print("3. Administrar configuración")
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
            menuAdminConfig()
        elif opcion == 4:
            break