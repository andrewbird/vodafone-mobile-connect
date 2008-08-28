if [ `id -u` -ne 0 ]
then
    zenity --error --text="Please run the installer as root or as a sudoer"
    exit 1
fi

#destroy me please :D
rm -f $0

file=`ls | grep vodafone`

echo "Installing the package"

yum install -y pyserial python-twisted pytz redhat-lsb
rpm -i $file

echo "Configuring the system..."

#udev configuration files
/sbin/udevcontrol reload_rules

for user in `zenity --entry --title="Enter allowed users" --text="Space separated user list"`
do
	id $user > /dev/null
	if [ $? -eq 1 ]; then echo "Invalid user $user"; continue; fi

    /usr/sbin/usermod -a -G uucp $user
done

echo
echo "Installation complete!"
echo
echo "Use vodafone-mobile-connect-card-driver-for-linux command or the direct access in your Internet menu in order to run the application."
