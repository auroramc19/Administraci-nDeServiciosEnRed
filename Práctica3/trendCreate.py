import rrdtool

def crearTrend(dispositivo):
    ret = rrdtool.create(f"./RRD/{dispositivo}.rrd",
                         "--start", 'N',
                         "--step", '60',
                         "DS:CPUload:GAUGE:60:0:100",  # GAUGE - Tipo de dato / limites -> :inferior:superior
                         "DS:RAMload:GAUGE:60:0:100",
                         "DS:OCTin:GAUGE:60:0:100",
                         "DS:OCTout:GAUGE:60:0:100",
                         "RRA:AVERAGE:0.5:1:24")
    if ret:
        print(rrdtool.error())
