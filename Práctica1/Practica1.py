from pysnmp.hlapi import *
from fpdf import FPDF


def agregarDispositivo():
    f = open('dispositivos.txt', 'a')
    host = input("Hostname/IP: ")
    comunidad = input("Comunidad: ")
    puerto = input("Puerto: ")
    f.write(host + ", " + comunidad + ", " + puerto)
    f.write("\n")
    f.close();


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

    generarReporte(host, comunidad, index+1)


def generarReporte(host, comunidad, index):
    MIB = '1.3.6.1.2.1'
    info = []

    # sistema operativo
    so = consultaSNMP(comunidad, host, MIB + '.1.1.0').split("Software: ")[1]
    info.append("Sistema Operativo: " + so)

    # nombre dispositivo
    hn = consultaSNMP(comunidad, host, MIB + '.1.5.0')
    info.append("Hostname: " + hn)

    # info contacto
    contc = consultaSNMP(comunidad, host, MIB + '.1.4.0')
    info.append("Contacto: " + contc)

    # info ubicacion
    ubi = consultaSNMP(comunidad, host, MIB + '.1.6.0')
    info.append("Ubicación: " + ubi)

    # num interfaces
    numInt = consultaSNMP(comunidad, host, MIB + '.2.1.0')
    info.append("Número de interfaces: " + numInt)

    for i in range(1, int(numInt)+1):
        nombre = consultaSNMP(comunidad, host, MIB + '.2.2.1.2.' + str(i))
        status = consultaSNMP(comunidad, host, MIB + '.2.2.1.7.' + str(i))
        info.append("Interfaz "+ str(i) + ": " + nombre + " Estatus: " + ("up" if status==1 else "down" if status==2 else "testing"))
        #print("Interfaz " + str(i) + ":" + )
        if i > 4:
            break

    print(*info, sep="\n")

    generarPDF(info, index)


def generarPDF(info, index):
    pdf = FPDF()
    pdf.add_page()

    ##header
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(80)
    pdf.cell(30, 10, 'Administración de Servicios en Red', 0, 0, 'C')
    pdf.ln(10)
    pdf.cell(80)
    pdf.cell(30, 10, 'Práctica 1: Adquisición de información usando SNMP', 0, 0, 'C')
    pdf.ln(20)

    ##body
    pdf.set_font('Arial', '', 11)
    for l in info:
        pdf.cell(30, 10, l, 0, 1)
    if(info[0].find('Windows')):
        pdf.image('windows.jpeg', 170, 40, 33)
    elif (info[0].find('Ubuntu')):
        pdf.image('ubuntu.png', 170, 40, 33)

    nombre = 'Dispositivo' + str(index) + '.pdf'
    pdf.output(nombre, 'F')

    print("Archivo PDF generado correctamente")


def consultaSNMP(comunidad, host, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        return str(varBinds[0][1])
        #for varBind in varBinds:
        #   varB = (' = '.join([x.prettyPrint() for x in varBind]))

def mostrarArchivoDispositivos():
    print("Dispositivos registrados:")
    i = 1
    with open("dispositivos.txt") as archivo:
        for linea in archivo:
            print(str(i) + ". " + linea)
            i = i + 1


def menu():
    opcion = 0
    while not (opcion == 4):
        print("\nAdquisición de información usando SNMP")
        print("1. Agregar dispositivo")
        print("2. Eliminar dispositivo")
        print("3. Generar reporte")
        print("4. Salir")

        opcion = int(input("\nElige una opción: "))

        if (opcion == 1):
            print("\n")
            agregarDispositivo();
        elif (opcion == 2):
            print("\n")
            eliminarDispositivo();
        elif (opcion == 3):
            print("\n")
            seleccionarDisp()
        elif (opcion == 4):
            break;


menu();
