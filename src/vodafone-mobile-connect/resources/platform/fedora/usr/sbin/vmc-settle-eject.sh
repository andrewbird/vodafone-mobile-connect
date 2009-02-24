#!/bin/bash

# Some devices will switch straight away, others like ZTE K3565-Z need to
# settle for a while before the eject will flip the device

DEVICE="$1"
WAIT="$2"

LOG=/var/log/vmc-settle-eject.log

echo called at "`date`" > ${LOG}

PATH=/usr/bin:/bin:/usr/sbin:/sbin

# eject device ASAP
eject ${DEVICE} >> S{LOG} 2>&1

( 
   sleep ${WAIT}

   if [ ! -e /dev/ttyUSB1 ] ; then 
      echo /dev/ttyUSB1 not found after ${WAIT} seconds >> ${LOG}
      echo ejecting again >> ${LOG}
      eject ${DEVICE} >> S{LOG} 2>&1
   fi

) < /dev/null > /dev/null 2>&1 &


