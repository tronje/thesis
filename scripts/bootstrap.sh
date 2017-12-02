#!/bin/bash

USER=$(whoami)
CONTAINER=ubuntu

# grab mkosi in case we don't have it
pacaur -S mkosi --noconfirm --noedit --needed
pacaur -S debootstrap ubuntu-keyring --asdeps --noconfirm --noedit --needed

# execute the rest of the script as root
exec sudo -i /bin/sh - << EOF

# this is where the machines live
cd /var/lib/machines

# if the machine already exists, do nothing
if [ ! -d $CONTAINER ]; then
    # bootstrap ubuntu xenial with mkosi
    mkosi -d ubuntu -r xenial --repositories main,universe -t directory -o $CONTAINER
fi

# to run Ubuntu in nspawn, we need to remove makedev, and install sudo
systemd-nspawn -D $CONTAINER /usr/bin/apt-get -y remove makedev
systemd-nspawn -D $CONTAINER /usr/bin/apt-get -y install sudo

# let's also install git
systemd-nspawn -D $CONTAINER /usr/bin/apt-get -y install git

# need to remove /etc/securetty to be able to log in with machinectl
systemd-nspawn -D $CONTAINER /bin/rm /etc/securetty

# ...and enable systemd-networkd to have internet
systemd-nspawn -D $CONTAINER /bin/systemctl enable systemd-networkd

# we'll also add a user...
systemd-nspawn -D $CONTAINER /usr/sbin/useradd -m -G sudo $USER

if [ ! -e /etc/systemd/nspawn/$CONTAINER.nspawn ]; then
    # basic config for this machine
    cat > /etc/systemd/nspawn/$CONTAINER.nspawn << EOM
    [Exec]
    Boot=1
    
    [Files]
    Bind=/run/user/1000/pulse:/run/user/host/pulse
    Bind=/home/$USER/thesis/data:/home/$USER/data
    
    [Network]
    VirtualEthernet=0
    EOM
fi

EOF
