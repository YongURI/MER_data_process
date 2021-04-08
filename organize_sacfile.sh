#!/bin/bash

#The folder where the sac files are stored
datadir="/home/yuy/Mermaid/mycode/Sacfile/St_sac"

Phase="p P PKP Pdiff PKiKP S SKS"

cd $datadir
#for evdir in `ls -d 20190823T000432`;do
for evdir in `ls -d 20*`;do
    cd $datadir/$evdir
    for sacfile in `ls -d *.sac`;do
        echo $sacfile
        evlon=`saclst evlo f $sacfile | awk '{print $2}'`
        evlat=`saclst evla f $sacfile | awk '{print $2}'`
        evdep=`saclst evdp f $sacfile | awk '{print $2}'`
        stlon=`saclst stlo f $sacfile | awk '{print $2}'`
        stlat=`saclst stla f $sacfile | awk '{print $2}'`
        stdep=`saclst stdp f $sacfile | awk '{print $2/1e3}'`
        ii=0
        for ph in `echo $Phase`;do
            ((ii=$ii+1))
            ph_t=`taup_time -h $evdep -evt $evlat $evlon -sta $stlat $stlon --stadepth $stdep -ph $ph \
            | grep " $ph  " | head -n1 | awk '{print $4}'`
            if [ -n "$ph_t" ];then
                echo "ch kt$ii $ph" >> micro.m
                echo "ch t$ii $ph_t" >> micro.m
            fi
        done
sac<< EOF
r $sacfile
ch o 0
m micro.m
wh
q
EOF
        rm micro.m
    done
done