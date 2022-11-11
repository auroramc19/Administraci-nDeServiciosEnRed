import time
import rrdtool
from getSNMP import consultaSNMP

def actualizarRRD(comunidad,host,namerrd):
    uni_pckts = 0
    ip_pckts = 0
    echo_icmp = 0
    segmentos_recv = 0
    dtg_udp = 0

    while 1:
        #Paquetes unicast que ha recibido una interfaz de red de un agente
        uni_pckts = str(
            consultaSNMP(comunidad,host,
                         '1.3.6.1.2.1.2.2.1.11.1')) #grupo 6 - TCP

        #Paquetes recibidos a protocolos IP, incluyendo los que tienen errores
        ip_pckts = str(
            consultaSNMP(comunidad,host,
                         '1.3.6.1.2.1.4.3.0'))

        #Mensajes ICMP echo que ha enviado el agente
        echo_icmp = str(
            consultaSNMP(comunidad,host,
                         '1.3.6.1.2.1.5.21.0'))

        #Segmentos recibidos, incluyendo los que se han recibido con errores
        segmentos_recv = str(
            consultaSNMP(comunidad,host,
                         '1.3.6.1.2.1.6.10.0'))

        #Datagramas entregados a usuarios UDP
        dtg_udp = str(
            consultaSNMP(comunidad,host,
                         '1.3.6.1.2.1.7.1.0'))

        valor = "N:" + str(uni_pckts) + ':' + str(ip_pckts) + ':' + str(echo_icmp) + ':' + str(segmentos_recv) + ':' + str(dtg_udp)
        #print (valor)
        rrdtool.update(f'./ArchivoRRD/{namerrd}.rrd', valor)
        rrdtool.dump(f'./ArchivoRRD/{namerrd}.rrd',f'./ArchivoRRD/{namerrd}.xml')
        time.sleep(1)

    if ret:
        print (rrdtool.error())
        time.sleep(300)