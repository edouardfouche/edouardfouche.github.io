---
layout: post
title:  "Automatic Train Timetable Display with Raspberry Pi"
date:   2017-07-17 08:00:00 +0100
comments: true
categories: Project RPi
---

I hate missing my train or arriving at the station to find out that my train is being delayed. This happens often, because German trains are so unpredictable ! Since I take the train every day for work, it is also a pain to check online every time I leave. I found a solution to alleviate this problem, using a Raspberry Pi. 

The Solution
------------

A Raspberry Pi computer shows in my corridor the departure times for the next trains for a set of chosen lines. Let me first show you how the solution looks like ! 

<br>
[![Ok Rpi, show me the next trains](/img/deutsche-bahn/Rpi.png)](https://www.youtube.com/watch?v=Ocr8C1BaPi8)
{:style="margin: auto"}
<br>

The display can show information about the next trains for various destinations. So this can be useful not only for me, but also for my girlfriend or our flatmate. 

Hardware Requirement
--------------------

- Raspberry Pi 1 B + [Sweetbox][Sweetbox]
- [Touchscreen Waveshare 3.5'][screen] on GPIO (< 30€)
- Power Supply [Nokia BT-AC10E][nokia] (< 10€)
- Nano Dongle Wifi LF-Link 150 Mb/s (< 10€)
- Sandisk 16 Gb 45 Mb/s (Smaller would also make it) (< 10€)

Note that if you take a Raspberry PI 3 you won't need the wifi dongle :). The display constructor provides a Raspbian image in which the external GPIO display is pre-configured. So it works out-of-the-box ! 

Then I bought some [on/off hook strips][tesa] from Tesa to put it in my corridor ! Hiding a part of the cable behind the mirror, it looks like this: 

<br>
![img](/img/deutsche-bahn/DSC_8839.JPG){:class="img-responsive"}
{:style="margin: auto"}
<br>


Software Requirement
--------------------

Getting an official Deutsch Bahn API key is difficult, if not impossible when you are not a business company. Instead, I used [schiene][schiene], a tiny Python library for interacting with Bahn.de, developed by [Kevin Kennell][kennell]. Basically it crawls the bahn.de mobile website to retrieve the next time table. It is like an unofficial API. I wrote a small script that wraps around it and handles the presentation of the results (including incidents and delay !) in the standard output with a periodic refresh of the results. It is available on my GitHub [here][dbtime]. 

This works for any connection in Germany. The script `dbtime.py` should be started with a few arguments, which specify the start and end stations of your trip. I've put a small bash script `launcher.sh` on the desktop of the Raspberry. It starts the program in the terminal with my desired connections:

```bash
#!/bin/sh
# launcher.sh
cd ~/github/deutsche-bahn-time-display/
sudo python dbtime.py "Stuttgart Hbf" "Karlsruhe HbF" "==KA==>" True
```

To make it executable, don't forget to do:

```bash
pi@rasp:~/Desktop$ sudo chmod 774 launcher.sh
```

Executing the script will display in the terminal the next trains from Stuttgart to Karlsruhe with the little prefix `==KA==>`, considering only direct connections (`True`). It looks like this:

```
1/1======================
==KA==> 23,36,82,143,165
IC  | 11:06 | 0:57 +0
RE  | 11:19 | 1:20 +0
IC  | 12:05 | 0:44 +0
IC  | 13:06 | 0:53 
ICE | 13:28 | 0:36 
.......
```

To make it look nice on the touchscreen, I changed the police to `DejaVu Sans Mono Book` with size 17 and changed the default dimensions of the terminal. To do so, just add the following line in the file `/usr/share/raspi-ui-overrides/applications/lxterminal.desktop`

```bash
Exec=lxtermnal --geometry=37x15
```

My friend Daniel is doing something similar, with a much fancier design, you can check it out [here][sancho].

Have a good trip ! 

[sancho]: https://hackaday.io/project/9690-tram-departure-time-indicator

[Sweetbox]: https://www.amazon.de/Sweetbox-Geh%C3%A4use-Raspberry-Modell-K%C3%BChlk%C3%B6rper/dp/B00IF9LIHC

[screen]: https://www.amazon.de/Waveshare-Raspberry-Resistive-Interface-Rapsberry-pi/dp/B00OZLG2YS/ref=sr_1_9?ie=UTF8&qid=1500132927&sr=8-9&keywords=waveshare+raspberry+pi+touchscreen

[tesa]:https://www.amazon.de/gp/product/B000WL4T8Q/ref=oh_aui_search_detailpage?ie=UTF8&psc=1
[kennell]: https://github.com/kennell
[schiene]: https://github.com/kennell/schiene
[dbtime]: https://github.com/edouardfouche/deutsche-bahn-time-display

[nokia]: https://www.amazon.de/Nokia-AC-10-Energiespar-Reiseladeger%C3%A4t-Micro-USB/dp/B002DPPKL4/ref=sr_1_1?s=computers&ie=UTF8&qid=1500133198&sr=1-1&keywords=Nokia+BT-AC10E