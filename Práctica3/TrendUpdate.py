import time
import rrdtool
from getSNMPs import consultaSNMP
from trendGraphDetection import graficarTrend
rrdpath = './RRD/'
carga_CPU = 0

def identificarRAM(comunidad,host):
    ram = ''
    i = 0
    while ram != 'Physical':
        i = i + 1
        ram = str(consultaSNMP(comunidad, host, '1.3.6.1.2.1.25.2.3.1.3.' + str(i))).split()[0]


    return str(i)

def actualizarTrend(comunidad,host,namerrd,nom_img):
    idRAM = identificarRAM(comunidad,host)
    storageSize = int(consultaSNMP(comunidad, host, '1.3.6.1.2.1.25.2.3.1.5.' + idRAM))
    storageAllocationUnits = int(consultaSNMP(comunidad, host, '1.3.6.1.2.1.25.2.3.1.4.' + idRAM))
    total_RAM = (storageSize * storageAllocationUnits) / 1000000000

    while 1:
        carga_CPU = int(consultaSNMP(comunidad,host,'1.3.6.1.2.1.25.3.3.1.2.6')) + int(consultaSNMP(comunidad,host,'1.3.6.1.2.1.25.3.3.1.2.7')) + int(consultaSNMP(comunidad,host,'1.3.6.1.2.1.25.3.3.1.2.8')) + int(consultaSNMP(comunidad,host,'1.3.6.1.2.1.25.3.3.1.2.9'))
        carga_CPU = carga_CPU / 4

        storageUsed = int(consultaSNMP(comunidad,host,'1.3.6.1.2.1.25.2.3.1.6.' + idRAM))
        carga_RAM_GB = (storageUsed * storageAllocationUnits) / 1000000000
        carga_RAM = (carga_RAM_GB * 100) / total_RAM

        if comunidad == 'AuroraMendez':
            oct_in = int(consultaSNMP(comunidad,host,'1.3.6.1.2.1.2.2.1.10.4'))
            oct_out = int(consultaSNMP(comunidad,host,'1.3.6.1.2.1.2.2.1.16.4'))
        else:
            oct_in = int(consultaSNMP(comunidad, host,'1.3.6.1.2.1.2.2.1.10.1'))
            oct_out = int(consultaSNMP(comunidad, host, '1.3.6.1.2.1.2.2.1.16.1'))

        valor = "N:" + str(carga_CPU) +":"+ str(carga_RAM) +":"+ str(oct_in) +":"+ str(oct_out)
        print (valor)

        rrdtool.update(f"RRD/{namerrd}.rrd", valor)
        #rrdtool.dump(f'./RRD/{namerrd}.rrd',f'./RRD/{namerrd}.xml')
        time.sleep(5)
        #graficarTrend(namerrd,nom_img+'_CPU','CPU Load','0','100','Carga del CPU','cargaCPU','CPUload',60,85,90, host.replace('.', '_'))
        graficarTrend(namerrd,nom_img+'_RAM','RAM Load','0','100', 'Carga de la RAM', 'cargaRAM', 'RAMload',65,80,90, host.replace('.', '_'))
        #graficarTrend(namerrd,nom_img+'_RED', y_label, lw_limit, up_limit, titulo, nom_e, def_e)

    if ret:
        print (rrdtool.error())
        time.sleep(300)
