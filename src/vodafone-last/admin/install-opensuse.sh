if [ `id -u` -ne 0 ]
then
    zenity --error --text="Please run the installer as root or as a sudoer"
    exit 1
fi

export DISPLAY=:0.0

#destroy me please :D
rm -f $0

file=`ls | grep vodafone`

echo "Installing the package"

zypper -n install python-twisted python-twisted-conch python-crypto lsb dbus-1-python
rpm -i pytz-2006p-7.1.noarch.rpm
rpm -i python-notify-0.1.0-0.pm.2.i586.rpm
rpm -i --nodeps $file

echo "Configuring the system..."

#udev configuration files
/sbin/udevcontrol reload_rules

for user in `zenity --entry --title="Enter allowed users" --text="Space separated user list"`
do
	id $user > /dev/null
	if [ $? -eq 1 ]; then echo "Invalid user $user"; continue; fi

    /usr/sbin/usermod $user -A uucp
done

echo
echo "Installation complete!"
echo
echo "Use vodafone-mobile-connect-card-driver-for-linux command or the direct access in your Internet menu in order to run the application."
