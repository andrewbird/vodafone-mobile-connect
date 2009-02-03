from networks import NetworkOperator

class SFRFrance(NetworkOperator):
    netid = ["20810"]
    name = "SFR"
    country = "France"
    type = ""
    smsc = "+33609001930"
    apn = "websfr"
    username = "websfr"
    password = "websfr"
    dns1 = "172.20.2.10"
    dns2 = "194.6.128.4"


class VodafoneSpain(NetworkOperator):
    netid = ["21401"]
    name = "Vodafone"
    country = "Spain"
    type = ""
    smsc = "+34607003110"
    apn = "ac.vodafone.es"
    username = "vodafone"
    password = "vodafone"
    dns1 = "212.73.32.3"
    dns2 = "212.73.32.67"


class MovistarSpain(NetworkOperator):
    netid = ["21402", "21407"]
    name = "Movistar"
    country = "Spain"
    type = ""
    smsc = "+34609090909"
    apn = "movistar.es"
    username = "movistar"
    password = "movistar"
    dns1 = "194.179.001.100"
    dns2 = "194.179.001.101"

class YoigoSpain(NetworkOperator):
    netid = ["21404"] + VodafoneSpain.netid
    name = "Yoigo"
    country = "Spain"
    type = ""
    smsc = "+34600000000"
    apn = "internet"
    username = "yoigo"
    password = "yoigo"
    dns1 = "10.8.0.20"
    dns2 = "10.8.0.21"

class VIPCroatia(NetworkOperator):
    netid = ["21910"]
    name = "VIP"
    country = "Croatia"
    type = ""
    smsc = "+385910401"
    apn = "data.vip.hr"
    username = "38591"
    password = "38591"
    dns1 = "212.91.97.3"
    dns2 = "212.91.97.4"


class VodacomSouthAfrica(NetworkOperator):
    netid = ["65501"]
    name = "Vodacom"
    country = "South Africa"
    type = ""
    smsc = "+27829129"
    apn = "internet"
    username = "vodafone"
    password = "vodafone"
    dns1 = "196.207.32.69"
    dns2 = "196.43.1.11"


class VodafoneItaly(NetworkOperator):
    netid = ["22210"]
    name = "Vodafone"
    country = "Italy"
    type = ""
    smsc = "+393492000200"
    apn = "web.omnitel.it"
    username = "vodafone"
    password = "vodafone"
    dns1 = "83.224.65.13"
    dns2 = "212.247.152.2"


class VodafonePortugal(NetworkOperator):
    netid = ["26801"]
    name = "Vodafone"
    country = "Portugal"
    type = ""
    smsc = "+351911616161"
    apn = "internet.vodafone.pt"
    username = "vodafone"
    password = "vodafone"
    dns1 = "212.18.160.133"
    dns2 = "212.18.160.134"


class VodafoneNetherlands(NetworkOperator):
    netid = ["20404"]
    name = "Vodafone"
    country = "Netherlands"
    type = ""
    smsc = "+316540881000"
    apn = "live.vodafone.com"
    username = "vodafone"
    password = "vodafone"
    dns1 = None
    dns2 = None


class NetComNorway(NetworkOperator):
    netid = ["24202"]
    name = "NetCom"
    country = "Norway"
    type = ""
    smsc = "+4792001000"
    apn = "internet"
    username = "internet"
    password = "internet"
    dns1 = "212.169.123.67"
    dns2 = "212.45.188.254"


class MobileOneSingapore(NetworkOperator):
    netid = ["52503"]
    name = "MobileOne"
    country = "Singapore"
    type = ""
    smsc = "+6596845999"
    apn = "sunsurf"
    username = "M1"
    password = "M1"
    dns1 = "202.65.247.151"
    dns2 = "202.65.247.151"


class TelkomSelIndonesia(NetworkOperator):
    netid = ["51010"]
    name = "TelkomSel"
    country = "Indonesia"
    type = ""
    smsc = "+6281100000"
    apn = "flash"
    username = "flash"
    password = "flash"
    dns1 = "202.3.208.10"
    dns2 = "202.3.210.10"

class SATelindoIndonesia(NetworkOperator):
    netid = ["51001"]
    name = "PT. SATelindo C"
    country = "Indonesia"
    type = ""
    smsc = "+62816124"
    apn = "indosat3g"
    username = "indosat"
    password = "indosat"
    dns1 = "202.155.46.66"
    dns2 = "202.155.46.77"

class IM3Indonesia(NetworkOperator):
    netid = ["51021"]
    name = "IM3"
    country = "Indonesia"
    type = ""
    smsc = "+62855000000"
    apn = "www.indosat-m3.net"
    username = "im3"
    password = "im3"
    dns1 = "202.155.46.66"
    dns2 = "202.155.46.77"

class ProXLndonesia(NetworkOperator):
    netid = ["51011"]
    name = "Pro XL"
    country = "Indonesia"
    type = ""
    smsc = "+62818445009"
    apn = "www.xlgprs.net"
    username = "xlgprs"
    password = "proxl"
    dns1 = "202.152.254.245"
    dns2 = "202.152.254.246"

class TMNPortugal(NetworkOperator):
    netid = ["26806"]
    name = "TMN"
    country = "Portugal"
    type = ""
    smsc = "+351936210000"
    apn = "internet"
    username = "tmn"
    password = "tmnnet"
    dns1 = None
    dns2 = None

class ThreeItaly(NetworkOperator):
    netid = ["22299"]
    name = "3"
    country = "Italy"
    type = ""
    smsc = "+393916263333"
    apn = "naviga.tre.it"
    username = "anon"
    password = "anon"
    dns1 = "62.13.171.1"
    dns2 = "62.13.171.2"

class ThreeAustralia(NetworkOperator):
    netid = ["50503"]
    name = "3"
    country = "Australia"
    type = ""
    smsc = "+61430004010"
    apn = "3netaccess"
    username = "*"
    password = "*"
    dns1 = None
    dns2 = None

class TimItaly(NetworkOperator):
    netid = ["22201"]
    name = "TIM"
    country = "Italy"
    type = ""
    smsc = "+393359609600"
    apn = "ibox.tim.it"
    username = "anon"
    password = "anon"
    dns1 = None
    dns2 = None

class WindItaly(NetworkOperator):
    netid = ["22288"]
    name = "Wind"
    country = "Italy"
    type = ""
    smsc = "+393205858500"
    apn = "internet.wind"
    username = "anon"
    password = "anon"
    dns1 = None
    dns2 = None

class VodafoneRomania(NetworkOperator):
    # Also known as Connex Romania
    netid = ["22601"]
    name = "Vodafone RO"
    country = "Romania"
    type = ""
    smsc = "+4092004000"
    apn = "internet.vodafone.ro"
    username = "internet.vodafone.ro"
    password = "vodafone"
    dns1 = "193.230.161.3"
    dns2 = "193.230.161.4"

if __name__ == '__main__':
    print VodafoneSpain()
