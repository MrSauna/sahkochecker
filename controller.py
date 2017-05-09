import urllib.request
import xml.etree.ElementTree as ET
import datetime
import pytz
from configuration import *
#import RPi.GPIO as GPIO


def getprices():

    global pricedict
    pricedict = {}

    timenow = datetime.datetime.utcnow()
    timez = timenow.strftime("%Y-%m-%dT%H:00Z")
    timeinaday = timenow + datetime.timedelta(1)
    timeinadayz = timeinaday.strftime("%Y-%m-%dT%H:00Z")

    req = urllib.request.Request(url="https://transparency.entsoe.eu/api?securityToken=" + token + "&DocumentType=A44&In_Domain=10YFI-1--------U&Out_Domain=10YFI-1--------U&TimeInterval=" + timez + "/" + timeinadayz)

    with urllib.request.urlopen(req) as f:
        response = str(f.read().decode("utf-8"))
        root = ET.fromstring(response)

        xmlns = "{"+root.tag[1:].split("}")[0]+"}"

        pricedict = {}

        for i in root.iter(xmlns + "Period"):
            starttime = datetime.datetime.strptime(i[0][0].text, "%Y-%m-%dT%H:00Z").replace(tzinfo=pytz.timezone("UTC"))
            for x in i.findall(xmlns+"Point"):
                pricedict[str(starttime + datetime.timedelta(hours=int(x[0].text)-1))] = x[1].text

    print(pricedict)
    print("hintoja palautettu: " + str(len(pricedict)))

def getweather():

    req = urllib.request.Request(url="http://api.openweathermap.org/data/2.5/forecast?id=660158&APPID="+appid+"&mode=xml")

    with urllib.request.urlopen(req):
        response = str(f.read().decode("utf-8"))
        root = ET.fromstring(response)

    for i in root.iter(""):

def shouldsave():

    nyt = datetime.datetime.now()

    if float(pricedict[str(nyt.strftime("%Y-%m-%d %H:00:00+00:00"))]) > maxprice:
        print("sähkön hinta: korkea")
        return True
    else:
        print("sähkön hinta: normaali")
        return


def saving(säästetään):
    chlist = [3,5]
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(chlist, GPIO.OUT)

    F = open("offsince", "r") #tiedosto ei saa olla tyhjä; pitää sisältää pelkestään jokin numero

    offsince = int(F.read().strip())

    F.close()

    F = open("offsince", "w")

    if säästetään == True and offsince <= 3:
        #GPIO.output(chlist, 0)
        F.write(str(offsince+1))
        print("säästetään")

    else:
        #GPIO.output(chlist, 1)
        print("ostetaan")
        F.write(str(0))


getprices()
saving(shouldsave())