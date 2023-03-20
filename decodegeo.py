from dataclasses import dataclass
from IPython.display import display
import folium
from tqdm import *
import geopy

gps_service = geopy.Nominatim(user_agent="South Korea")


@dataclass
class Latitude:
    degree:int=None
    minute:int=None
    second:int=None
    accuracy:int=None

@dataclass
class Longitude:
    degree:int=None
    minute:int=None
    second:int=None
    accuracy:int=None

def get_addr(x,y):    
    geoloc = gps_service.reverse(str(x)+", "+str(y))
    return geoloc.address

def dms_2_degree(dms):
    deg,minutes,seconds = dms.split(".")
    return(float(deg) + float(minutes)/60 + float(seconds)/(60*60))

def int_2_dms(dat):
    dat = (dat / 100) / 3600
    degree = int(dat)
    dat = 60 * (dat - degree)
    minute = int(dat)
    dat = 60 * (dat - minute)
    second = int(dat)

    return str(degree), str(minute), str(second)

def parse_gps(dat):
    lat = int.from_bytes(dat[0:4], byteorder='big')
    log = int.from_bytes(dat[4:8], byteorder='big')
    
    Latitude(),Longitude()

    Latitude.degree, Latitude.minute,Latitude.second  = int_2_dms(lat)
    Longitude.degree, Longitude.minute,Longitude.second  = int_2_dms(log)

    return [".".join([Latitude.degree,Latitude.minute,Latitude.second]),".".join([Longitude.degree,Longitude.minute,Longitude.second])]
    

#read data
data_block = open('GPSTrack.dat','rb').read()
header = data_block[0:8]
data_block=data_block[8:]
CRC = data_block[-9:]

gps_dat = []
for i in trange(0,len(data_block),0xc):
    try:
        dat = data_block[i:i+0xc][::-1]
        dms = parse_gps(dat)    
        loc = get_addr(dms_2_degree(dms[0]),dms_2_degree(dms[1]))
        dms.append(loc)
        gps_dat.append(dms)
    except:
        continue



#mapping
Map = folium.Map(location=[dms_2_degree(gps_dat[0][0]),dms_2_degree(gps_dat[0][1])],zoom_start=12,tiles="Stamen Terrain",)
for dms in gps_dat: 
    folium.Marker(location=[dms_2_degree(dms[0]),dms_2_degree(dms[1])],icon=folium.Icon(color="red")).add_to(Map)
Map.save('GPSTrack_Map.html')