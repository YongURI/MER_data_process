#!/home/yuy/anaconda3/envs/seism27/bin/python
import obspy
from obspy import read_events, read, read_inventory
from obspy.clients.fdsn.mass_downloader import RectangularDomain, \
    Restrictions, MassDownloader
from obspy.clients.fdsn import Client
import write_cat
from os import listdir, makedirs
from os.path import join, exists

starttime = obspy.UTCDateTime("2019-1-1T00:00:00")
endtime = obspy.UTCDateTime("2021-1-1T00:00:00")
outpath = '/home/yuy/Mermaid/mycode/Sacfile/St_sac'

isall_ev=0 # 0: read event catlogue from .xml; 1: download event catlogue from IRIS
if isall_ev == 1:
    client = Client("IRIS")
    cat = client.get_events(starttime=starttime,endtime=endtime,minmagnitude=6.5,
                        magnitudetype="Mw" ,catalog="NEIC PDE")
else:
    cat=read_events('MER_ev.xml')
write_cat.write_cat(cat,'catlogue.txt')
domain1 = RectangularDomain(minlatitude=-40, maxlatitude=10, 
                            minlongitude=160, maxlongitude=180)
domain2 = RectangularDomain(minlatitude=-40, maxlatitude=10, 
                            minlongitude=-180, maxlongitude=-110)                            

mdl = MassDownloader(providers=["RESIF","IRIS","RASPISHAKE"])


for evt in cat.events:
#origin_time = obspy.UTCDateTime(2011,3,11,5,47,32)
    origin_time = evt.origins[0].time
    print (origin_time)
    evlat = evt.origins[0].latitude
    evlon = evt.origins[0].longitude
    evdep = evt.origins[0].depth/1e3
    evmag = evt.magnitudes[0].mag

    if origin_time > endtime or origin_time < starttime:
        continue 
    restrictions = Restrictions(
        starttime=origin_time,
        endtime=origin_time + 1800,
        reject_channels_with_gaps=True,
        minimum_length=0.95)
    dirname = origin_time.strftime("%Y%m%dT%H%M%S")
    mdl.download(domain1, restrictions, mseed_storage="St_mseed/"+dirname,
            stationxml_storage="stations")
    mdl.download(domain2, restrictions, mseed_storage="St_mseed/"+dirname,
            stationxml_storage="stations")
    for mseed_f in listdir(join("./St_mseed",dirname)):
        net = mseed_f.split(".")[0]
        stnm = mseed_f.split(".")[1]
        st = read(join('./St_mseed',dirname,mseed_f))
        st_xml = join('./stations',net+'.'+stnm+'.xml')
        inv = read_inventory(st_xml)
        stlat = inv.networks[0].stations[0].latitude
        stlon = inv.networks[0].stations[0].longitude
        stele = inv.networks[0].stations[0].elevation
        st[0].stats.sac = {}
        st[0].stats.sac[u'stlo'] = stlon
        st[0].stats.sac[u'stla'] = stlat
        st[0].stats.sac[u'stdp'] = stele
        st[0].stats.sac[u'evlo'] = evlon
        st[0].stats.sac[u'evla'] = evlat
        st[0].stats.sac[u'evdp'] = evdep
        st[0].stats.sac[u'mag'] = evmag
        pre_filt = (0.01,0.02,20,30)
        st.remove_response(inventory=inv, output='DISP', pre_filt=pre_filt)
        if not exists(join(outpath,dirname)):
            makedirs(join(outpath,dirname))
        st.write(join(outpath,dirname,mseed_f.replace('mseed','sac')),format='SAC')
    
    