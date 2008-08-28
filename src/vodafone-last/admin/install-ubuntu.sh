# destroy me please :D
rm -f $0

file=`ls | grep vodafone`

echo "Installing the package"

gksudo "dpkg -i $file"
gksudo "apt-get install --fix-broken -y -q"
gksudo "dpkg -i $file"

echo "Configuring the system..."

# udev configuration files
gksudo /sbin/udevcontrol reload_rules

echo
echo "Installation complete!"
echo
echo "Use vodafone-mobile-connect-card-driver-for-linux command or the direct access in your Internet menu in order to run the application."
