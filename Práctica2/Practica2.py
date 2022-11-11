from pysnmp.hlapi import *
from fpdf import FPDF
from datetime import datetime
from graphRRD import graphCreate
from CreateRRD import crearRRD
from updateRRD import actualizarRRD
from threading import Thread

def agregarDispositivo():
    f = open('dispositivos.txt', 'a')
    host = input("Hostname/IP: ")
    comunidad = input("Comunidad: ")
    puerto = input("Puerto: ")
    f.write(host + ", " + comunidad + ", " + puerto)
    f.write("\n")
    f.close();

    rrd = 'practica2_D'+host.replace('.','_')
    crearRRD(rrd)
    t = Thread(name="updateRRD", target=actualizarRRD, args=(comunidad, host, rrd))
    t.start()
    print("Inicio sondeo")


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

    generarReporte(host, comunidad, puerto, index + 1)


def mostrarArchivoDispositivos():
    print("Dispositivos registrados:")
    i = 1
    with open("dispositivos.txt") as archivo:
        for linea in archivo:
            print(str(i) + ". " + linea)
            i = i + 1


def generarReporte(host, comunidad, puerto, index):
    MIB = '1.3.6.1.2.1'
    info1 = []
    info = []

    #device
    dev = consultaSNMP(comunidad, host, puerto, MIB + '.1.5.0')
    info1.append(dev)

    #description
    d = consultaSNMP(comunidad, host, puerto, MIB + '.1.6.0')
    info1.append(d)

    #NAS-IP-Address
    nia = host
    info.append(nia)

    #NAS-Port
    np = puerto
    info.append(np)

    #User-Name
    un = consultaSNMP(comunidad, host, puerto, MIB + '.1.5.0')
    info.append(un)

    #Acct-Input-Octets
    aio = consultaSNMP(comunidad, host, puerto, MIB + '.2.2.1.10.1')
    info.append(aio)

    #Acct-Output-Octets
    aoo = consultaSNMP(comunidad, host, puerto, MIB + '.2.2.1.16.1')
    info.append(aoo)

    #Acct-Session-Id
    asi = str(index)
    info.append(asi)

    # Acct-Session-Time
    ast = consultaSNMP(comunidad, host, puerto, MIB + '.1.3.0')
    info.append(ast)

    # Acct-Input-Packets
    aip = consultaSNMP(comunidad, host, puerto, MIB + '.2.2.1.11.1')
    info.append(aip)

    # Acct-Output-Packets
    aop = consultaSNMP(comunidad, host, puerto, MIB + '.2.2.1.17.1')
    info.append(aop)

    #print(*info, sep="\n")

    crearGraficas(info1, info, index,host)


def consultaSNMP(comunidad, host, puerto, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, int(puerto))),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        print(str(varBinds[0][1]))
        return str(varBinds[0][1])

def crearGraficas(info1, infoR, index,host):
    imagenes = []
    index = str(index)

    titulo = 'Paquetes unicast que ha recibido\n una interfaz de red de un agente'
    graphCreate('uni_pckts'+index,'pUnicastRec','./ArchivoRRD/practica2_D'+host.replace('.','_'),'Paquetes',titulo,'#8A2BE2','Paquetes unicast')
    imagenes.append(f'./GraficasRRD/uni_pckts{index}.png')

    titulo = 'Paquetes recibidos a protocolos IP,\n incluyendo los que tienen errores'
    graphCreate(f'ip_pckts'+index,'pRecibidosIP', './ArchivoRRD/practica2_D'+host.replace('.','_'), 'Paquetes', titulo, '#FF7F50', 'Paquetes recibidos')
    imagenes.append(f'./GraficasRRD/ip_pckts{index}.png')

    titulo = 'Mensajes ICMP echo que\n ha enviado el agente'
    graphCreate('echo_icmp'+index,'mICMPEchoEnv', './ArchivoRRD/practica2_D'+host.replace('.','_'), 'Mensajes', titulo, '#6495ED', 'Mensajes ICMP echo')
    imagenes.append(f'./GraficasRRD/echo_icmp{index}.png')

    titulo = 'Segmentos recibidos, incluyendo\n los que se han recibido con errores'
    graphCreate('segmentos_recv'+index, 'segmentosRec', './ArchivoRRD/practica2_D'+host.replace('.','_'), 'Segmentos', titulo, '#006400', 'Segmentos recibidos')
    imagenes.append(f'./GraficasRRD/segmentos_recv{index}.png')

    titulo = 'Datagramas entregados a usuarios UDP'
    graphCreate('dtg_udp'+index, 'datagramasUDP', './ArchivoRRD/practica2_D'+host.replace('.','_'), 'Datagramas', titulo, '#8B0000', 'Datagramas entregados')
    imagenes.append(f'./GraficasRRD/dtg_udp{index}.png')

    generarPDF(info1, infoR, index, imagenes)

def generarPDF(info1, infoR, index, imagenes):
    pdf = FPDF()
    pdf.add_page()

    fecha = str(datetime.now()).split(" ")[0]
    hora = str(datetime.now()).split(" ")[1].split(".")[0].replace(':', '\'')
    nombre = 'Dispositivo' + '1' + '-' + fecha + 'T' + hora + '.pdf'

    ##header
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(80)
    pdf.cell(30, 10, 'Administración de Servicios en Red', 0, 0, 'C')
    pdf.ln(6)
    pdf.cell(80)
    pdf.cell(30, 10, 'Práctica 2 Sistema de administración de Contabilidad', 0, 0, 'C')
    pdf.ln(6)
    pdf.cell(80)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(30, 10, 'Aurora Méndez Castañeda Boleta: 2020630290 Grupo: 4CM13', 0, 0, 'C')
    pdf.ln(15)

    ##body
    # encabezado
    pdf.set_font('Arial', '', 11)
    pdf.cell(40, 15, 'version: 1\n', 0, 0)
    pdf.ln(4)
    pdf.cell(40, 15, 'device: ' + info1[0], 0, 0)
    pdf.ln(4)
    pdf.cell(40, 15, 'description: ' + info1[1], 0, 0)
    pdf.ln(4)
    pdf.cell(40, 15, 'date: ' + fecha + 'T' + hora, 0, 0)
    pdf.ln(4)
    pdf.cell(40, 15, 'defaultProtocol: radius', 0, 0)
    pdf.ln(10)

    # info sistema
    info = ['#NAS-IP-Address', '#NAS-Port', '#User-Name', '#Acct-Input-Octets', '#Acct-Output-Octets',
            '#Acct-Session-Id', '#Acct-Session-Time', '#Acct-Input-Packets', '#Acct-Output-Packets']
    pdf.cell(40, 15, 'rdate: ' + fecha + 'T' + hora, 0, 0)
    pdf.ln(4)

    for valor_info, valor_infoR in zip(info, infoR):
        pdf.cell(40, 15, valor_info, 0, 0)
        pdf.ln(4)
        pdf.cell(40, 15, valor_infoR, 0, 0)
        pdf.ln(4)

    #imagenes
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 15, 'Gráficas\n', 0, 0)

    x = 30
    y = 20
    w = 150
    for i in imagenes:
        pdf.image(i, x, y, w)
        y += 55

    pdf.output('./Reportes/'+nombre, 'F')

    print("Archivo PDF generado correctamente")


if __name__ == "__main__":
    opcion = 0

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
