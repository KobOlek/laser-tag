![Laser-Tag Alpha](https://i.imgur.com/AfN4zLe.png)

# LaserTag-α 🐍

Software realisation of LaserTag-α, made with Python and cv2. Requires Camera Module and a laser pointer.



## Requirements 📖

To deploy this project, install Raspberry Pi OS, then completely update it:
```bash
sudo apt update && sudo apt full-upgrade
```
For better experience, hide the taskbar and make it as small as possible.
Create a venv with all needed default dependencies:
```bash
python3 -m venv --system-site-packages env
```
To install all dependencies:
```bash
  pip install -r requirements.txt
```
## FAQ ❓

#### Mouse won't move/code is crushing/etc.

The reason for that is Wayland. Our code is optimized for x11 (we don't care about how bad x11 is and how Wayland is better). After updating and upgrading, run
```bash
sudo raspi-config
```
And change the displaying method.

#### Why are you using Tkinter?

As a workaround for mouse problem, we made a simple fix - move imshow window to the bottom, and hide it with tkinter window of same color as the background.

## Planned ‼️

- Web app/mobile app for changing things and calibrating

- More game modes

- Releasing already configured OS as sd-card dump.

## Authors 🇺🇦

- [@olekbliter](https://github.com/olekbliter) - HTML frontend, team lead, original idea author,
- [@kobolek](https://github.com/kobolek) - Python backend, original realisation,
- [@olehm208](https://github.com/olehm208) - Linux port, optimization, refactoring, mouse problems fix. 




