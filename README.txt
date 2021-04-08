1. get_MER_ev.py:
   This script is used for building the event catlogue that are recorded by MERMAIDs
   Input: identified.txt from Omnia;
   Output: MER_catlogue.txt .txt file of catlogue
           MER_ev.xml .xml file used in Obspy later

2. organize_Mer_sacfile.sh
    This script is used to copy the sac file of MERMAIDs to folder named by the date of earthquake
    Input: identified.txt firstarrivals.txt from Omnia
           MER_catlogue.txt from  get_MER_ev.py
    Output: $outdir/$evdir/???.sac
    Note: $Startdate and $Enddate must be changed before excuting the script
          o of the head of sac file is the origin time of the earthquake
          t1-t7 in .sac files are used for traveltimes calculated by Taup 
          t9 is used for the arrival time from Omnia

3. Get_waveform_IRIS.py
    This script is used for downloading the Seismic date based on the catlugue of between a time 
    period from IRIS.
    Input: $starttime and $endtime the analysis time period 
           MER_ev.xml from get_MER_ev.py
    Output: ./stations/*.xml station file
            ./St_mseed/$dirname/*.mseed .mseed file downloaded
            ./St_sac/$dirname/*.sac .sac file converted from .mseed the event and station information is writen 
                in the head and the instrument's reponse is removed and the output sac file is displacement

4. write_stinfo.py
    This script is used to build a staion list file St_info.txt from the .xml file from Get_waveform_IRIS.py

5. organize_sacfile.sh
    This script is used to write the calculated arrival time in the .sac files from Get_waveform_IRIS.py


