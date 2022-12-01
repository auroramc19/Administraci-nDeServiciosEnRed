import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getSNMPs import consultaSNMP

COMMASPACE = ', '
# Define params
rrdpath = 'RRD/'
imgpath = 'IMG/'
fname = 'trend.rrd'

mailsender = "dummycuenta3@gmail.com"
mailreceip = "dummycuenta3@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = 'dvduuffmlhspbmjj'

def send_alert_attached(subject,grafica,nameF,titulo):
    """ Envía un correo electrónico adjuntando la imagen en IMG
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    fp = open(imgpath+grafica, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    body = 'Monitorización del rendimiento de un agente usando SNMP\n'
    body = f'Revisar {titulo}\n'
    inventario = open(f'Inventario/inventario_{nameF}.txt','r')
    for i in inventario:
        body += i
    body = MIMEText(body)
    msg.attach(body)
    inventario.close()
    msg.attach(img)
    s = smtplib.SMTP(mailserver)

    s.starttls()
    # Login Credentials for sending the mail
    s.login(mailsender, password)

    s.sendmail(mailsender, mailreceip, msg.as_string())
    s.quit()