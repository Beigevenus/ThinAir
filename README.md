# ThinAir
ThinAir is a software implementation allowing virtually any combination of a webcam and projector (or screen) to act as a digital whiteboard. It utilizes MediaPipe to track the user's hand, and translates specific hand poses to actions in the system, such as drawing by extending the index finger, and opening the tool/color menu by making a fist.

ThinAir has been produced as an undergraduate project at Aalborg University, Denmark.

## Supported Hardware and OS
The system has been tested with various combinations of projectors, webcams, and operating systems. The following is a list of components that have been officially tested and have been determined to be fully supported, although we assume that it will work with essentially any combination of projector, webcam, and OS as long as these are compatible with each other.

**Projectors and Screens:**
 - ASUS P3E DLP-projector
 - A Samsung TV

**Webcams:**
 - Razer Kiyo
 - Gearlab G640 HD
 - Logitech V-U0018

**Operating Systems:**
 - Windows 10
 - Ubuntu 20.04

## How To Use?
### Setup
ThinAir has been tested and works with Python 3.9. To use the software, first, install the requirements:
```
pip install -r requirements.txt
```

Then, ThinAir can be run with:
```
py main.py
```

### Usage
When ThinAir is run, there is a few keyboard shortcuts, which hold significance:
 - s: opens the settings menu, and writes the chosen configuration to `config.json`
 - t: saves the current drawing to `drawing.json`, which is loaded upon startup

To calibrate the camera, make sure the entire projected surface or screen is within view, and left-click on each of the four corners. A blue square should now highlight the projected area. If this is not the case, left-click once to reset the calibration, and try again.

You can now use your hand to draw on the projected surface.

#### Hand Poses
| **Name**     | **Pose**                                            | **Functionality**                                  |
|--------------|-----------------------------------------------------|----------------------------------------------------|
| Current Tool | Extend index finger, retract all other fingers      | Uses the currently selected tool (drawing/erasing) |
| Tool Menu    | Make a fist, and move your hand to the desired tool | Opens the tool/color menu                          |
