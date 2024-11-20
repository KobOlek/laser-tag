
# LaserTag-α

Software realisation of LaserTag-α, made with Python and CV2. Requires Camera Modul and a laser pointer.



## Requirements 

To deploy this project, install Raspberry Pi OS, then completely update it:
```bash
sudo apt update && sudo apt full-upgrade
```
For better experience, hide the taskbar and make it as small as possible.
To install all dependencies:
```bash
  pip install -r requirements 
```



## FAQ

#### My mouse doesn't move!

This is a general problem with our project that we can't fix at this moment. The temporary solution to fix this is to run:
```bash
sudo python main.py
```
#### If the above doesn't work

The reason for that is Wayland. Our code is optimized for x11 (we don't care about how bad x11 is and how Wayland is better). After updating and upgrading, run
```bash
sudo raspi-config
```
And change the displaying method.




