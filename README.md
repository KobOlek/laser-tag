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

## License 📄

MIT License

Copyright (c) 2024 3xO

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



