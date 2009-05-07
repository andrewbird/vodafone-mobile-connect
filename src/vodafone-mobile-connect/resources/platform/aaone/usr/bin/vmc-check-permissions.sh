#!/bin/bash

#This shell script checks permissions and change them if they are not correct.


#Paths need to be absolute.
pppd_file="/usr/sbin/pppd"
chap_secrets_file="/etc/ppp/chap-secrets"
pap_secrets_file="/etc/ppp/pap-secrets"
peers_file="/etc/ppp/peers"
ipup_file="/etc/ppp/ip-up.local"
ipdown_file="/etc/ppp/ip-down.local"


function getGroup () {
    echo $(stat -c %G $1)
}


function getPermissionsOctal () {
    echo $(stat -c %a $1)
}


# $1 file_name
# $2 group_name
function setGroup () {
    if [[ $(getGroup $1) != $2 ]];
    then 
#	echo "setting $1 to group $2";
	chown ":$2" $1 ;
    else 
#	echo "group correct";
	:
    fi	
}


# $1 file_name
# $2 octal permissions
function setPermissions () {
    if [[ $(getPermissionsOctal $1) != $2 ]];
    then
# 	echo "setting $1 to permissions $2";
	chmod $2 $1;
    else
#	echo "permissions are correct";
	:
    fi
}


setGroup $chap_secrets_file "dip"
setPermissions $chap_secrets_file 660

setGroup $pap_secrets_file "dip"
setPermissions $pap_secrets_file 660

setGroup $peers_file "dip"
setPermissions $peers_file 775

setGroup $pppd_file "dip"
setPermissions $pppd_file 4754


# Compares $1 and $2 and if they are different, $2 is overwritten by $1
function compareAndSet () {
    if [[ -f $1 ]];
    then
	# $1 file exists.
	if [[ ! -f $2 ]];
	then
	    # $1 exist and $2 does not exist.
	    cp -f $1 $2
	else
	    # $1 and $2 exist.
	    cmp $1 $2
	    if [[ $? -eq 1 ]];
	    then
#		echo "files are different";
		mv -f $2 "$2.bak"
		cp -f $1 $2
	    fi
	fi
    fi
}


compareAndSet "${ipup_file}.vmc" $ipup_file
compareAndSet "${ipdown_file}.vmc" $ipdown_file




