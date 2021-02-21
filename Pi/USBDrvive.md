
***

# External Storage (USB Stick)

In addition to the RaspberryPi, we need a storage device for all the data we will collect.
I'm not really sure at this time what size we need, so I'll go big, and use the [Samsung 32GB USB 3.0 Flash Drive Fit](https://www.amazon.com/Samsung-Flash-Drive-MUF-32BB-AM/dp/B013CCTOC2) from amazon.
First, find any unintentional mounts from plugging in the flash drive. (Note: the procedures below assume the device is /dev/sda, and therefore the partition is /dev/sda1.  Should the next command display a different device, you must adapt as required.)

  ```
  df -h
  ```

look for devices mounted to /dev/sda*, and unmount them.  For example if you see a directory mounted on /dev/sda1, as I did with my Samsung-Flash-Drive-MUF-32BB, then run this command to unmount it.

<br>

![alt text][DFH]

[DFH]: https://github.com/DonBower/HamGoBox/blob/master/Pi/DF%20-h%20output.png "df -h output example"

<br>


  ```
  sudo umount /dev/sda1
  ```

Next, *and this is destructive*, remove any partitions, and create a new, fresh one.

  ```
  sudo fdisk /dev/sda
  p # This will print all the partitions
  d # This will delete the last partition. Repeat as required to delete all partitions
  n # This will create a new partition.  Take all the defaults.
  w # Rewrite the new partition table.
  ```

Now, format the new partition for ext4 file system.

  ```
  sudo mkfs.ext4 -L HamGoBox /dev/sda1
  ```

The follow steps will allow the USB drive to be persistently mounted.

```
sudo mkdir /mnt/usbstick
sudo chmod 777 /mnt
sudo chmod 777 /mnt/usbstick
sudo tee -a /etc/fstab <<EOF
LABEL=HamGoBox     /mnt/usbstick   ext4    defaults          0       1
EOF
sudo mount -a
```

You should now be able to `df -h` and see the /dev/sda1 mounted on /mnt/usbstick.
