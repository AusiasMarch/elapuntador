[Install raspbian on usb boot from SD card](https://www.stewright.me/2013/05/install-and-run-raspbian-from-a-usb-flash-drive/)

* `sudo umount /dev/sdb1`
* `sudo umount /dev/sdb2`
* `sudo dd bs=4M if=2019-09-26-raspbian-buster-lite.img of=/dev/sdb`
* `touch /media/ausias/boot1/ssh` 
* `perl -i.bck -pe's/$/ ip=192.168.1.30/ if eof' /media/ausias/boot1/cmdline.txt `
* `sed -i 's/root=\S*\ /root=\/dev\/sda2\ /g' /media/ausias/boot1/cmdline.txt`
* `cp -r /media/ausias/boot1/ /media/ausias/boot`
* `ssh-keygen -f "/home/ausias/.ssh/known_hosts" -R "192.168.1.30"`
* `ssh pi@192.168.1.30 mkdir /home/pi/.ssh` (passwd: raspberry)
* `scp .ssh/id_rsa_battlestarGalactica.pub pi@192.168.1.30:.ssh/authorized_keys`
* `scp ~/.ssh/id_rsa_raspi raspi:.ssh/id_rsa`
* `scp ~/.ssh/id_rsa_raspi.pub raspi:.ssh/id_rsa.pub`
* `ssh raspi`
* `passwd`
* `sudo fdisk /dev/sda`
* Note of the start position for the linux partition sda2 (532480)
* `d`
* `2`
* `n`
* `p`
* `2`
* `(532480)`
* Enter
* `Yes`
* `w`
* `sudo reboot`
* `sudo resize2fs /dev/sda2`
* `sudo reboot`
* `sudo apt -y update`
* `sudo apt -y upgrade`
* `sudo apt -y install git`
* `git clone git@github.com:AusiasMarch/mi_apio.git`
* ``
* ``
* ``
* ``
